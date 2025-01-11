from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import mysql.connector
from mysql.connector import Error
import time
import redis


def acquire_sql_lock(connection, function_to_execute):
    try:
        lock_name = 'lock_1234'
        timeout = 3
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"SELECT GET_LOCK('{lock_name}', {timeout});")
            result = cursor.fetchone()
            
            if result[0] == 1:
                print(f"Lock '{lock_name}' acquired. Executing {function_to_execute.__name__}.")
                if callable(function_to_execute):
                    function_to_execute()
                print(f"Releasing lock '{lock_name}'.")
            else:
                print(f"Lock '{lock_name}' already exists. Could not acquire.")
    except Error as e:
        print("Error while connecting to MySQL:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")




def acquire_redis_lock(redis_connection, function_to_execute):
    try:
        lock_name = 'lock_1234'
        timeout = 1
        lock = redis_connection.lock(lock_name, timeout=timeout)
        if lock.acquire(blocking=False):
            print(f"Lock '{lock_name}' acquired. Executing {function_to_execute.__name__}.")
            if callable(function_to_execute):
                function_to_execute()
            lock.release()
            print(f"Lock '{lock_name}' released.")
        else:
            print(f"Lock '{lock_name}' could not be acquired (already held).")
    except redis.RedisError as e:
        print("Error while using Redis:", e)






def start_cron_with_expression(connection, my_custom_function, cron_expression,type):
    if type == 'mysql':
        scheduler = BackgroundScheduler()
        trigger = CronTrigger.from_crontab(cron_expression)  # Use cron-like syntax
        scheduler.add_job(acquire_sql_lock, trigger, args=[connection, my_custom_function])
        scheduler.start()
    elif type == 'redis':
        scheduler = BackgroundScheduler()
        trigger = CronTrigger.from_crontab(cron_expression)  
        scheduler.add_job(acquire_redis_lock, trigger, args=[connection, my_custom_function])
        scheduler.start()
    else:
        print("Please provide correct lock name \nAvailable locks - redis or mysql")
        return 1



# Example: Pass a full cron expression
# connection=None
# cron_expression = "*/1 * * * *"
# start_cron_with_expression(connection, "abc",cron_expression,"rediss")

