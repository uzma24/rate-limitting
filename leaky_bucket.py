from time import time
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

redis.flushall()
fixed_bucket_capacity = 5
leak_rate_per_min = 3

def leaky_bucket(userID, reqID, timeStamp):
    if (not redis.exists(userID)):
        user_dict = {"time_stamp": timeStamp, "current_bucket_capacity": fixed_bucket_capacity-1}
        redis.hmset(userID, user_dict)
        return 'True: processed reqID: '.join(reqID) 
    else:
        user_bucket_from_redis = redis.hgetall(userID)
        current_req_time = timeStamp/60 ##to get time in minutes
        delta_time_elapsed = current_req_time - user_bucket_from_redis["time_stamp"]
        
        if(delta_time_elapsed == 0): 
            ##request is still within same minute/that one minute window range, hence no leak has happend yet
            if(user_bucket_from_redis["current_bucket_capacity"] > 0):
                temp_bucket_capacity = user_bucket_from_redis["current_bucket_capacity"]
                redis.hset(userID, "current_bucket_capacity",(user_bucket_from_redis["current_bucket_capacity"])-1)
                return 'True: processed reqID: '.join(reqID)
        else:
            ## calculate how much leak happend/ how much space in bucket emptied in time elapsed 
            leak_from_bucket = delta_time_elapsed*leak_rate_per_min
            new_bucket_capacity = user_bucket_from_redis["current_bucket_capacity"] + leak_from_bucket
            if (new_bucket_capacity == 0):
                return 'False: cannot process reqID: '.join(reqID)
            elif (new_bucket_capacity < fixed_bucket_capacity):
                redis.hset(userID, {"current_bucket_capacity": new_bucket_capacity-1, "time_stamp": time.Now()})
                return 'True: processed reqID: '.join(reqID)
            elif(new_bucket_capacity > fixed_bucket_capacity):
                redis.hset(userID, {"current_bucket_capacity": fixed_bucket_capacity-1, "time_stamp": time.Now()})
                return 'True: processed reqID: '.join(reqID)
            else: 
                return 'False: cannot process reqID: '.join(reqID)

    
    return 'False: cannot process reqID: '.join(reqID)

for i in range(50):
    request = f"Request {i+1}"
    print(leaky_bucket("user1", request))

        





