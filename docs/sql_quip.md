
## Query 1 Find the month-over-month percentage change for monthly active users (MAU). 

**Schema (PostgreSQL v13)**

    CREATE TABLE logins (
    user_id int,
    user_date timestamp  
    );
    
    
    INSERT INTO logins (user_id, user_date)
    VALUES
    (1, '2018-07-01'),
    (2, '2018-09-02'),
    (3, '2018-07-04'),
    (1, '2018-08-11'),
    (1, '2018-07-09'),
    (3, '2018-07-25'),
    (5, '2018-07-25'),
    (6, '2018-07-25'),
    (7, '2018-07-25'),
    (1, '2018-07-25'),
    (2, '2018-11-02'),
    (5, '2018-07-25'),
    (5, '2018-08-25'),
    (7, '2018-10-25'),
    (5, '2018-11-25'),
    (6, '2018-11-25')
    ;

---

**Query #1**

    WITH test AS 
    (
      SELECT 
      DATE_TRUNC('month', user_date) month_ts,
      COUNT(DISTINCT user_id) dist_user
      FROM logins
      GROUP BY DATE_TRUNC('month', user_date)
    )
    
    SELECT
    a.month_ts previous_mnt,
    a.dist_user prev_user_cnt,
    b.month_ts current_mnt,
    b.dist_user curr_user_cnt,
    ROUND(100.0*(b.dist_user - a.dist_user)/a.dist_user,2) AS percentage_change
    FROM test a
    JOIN test b 
    ON a.month_ts = b.month_ts - interval '1 month';

| previous_mnt             | prev_user_cnt | current_mnt              | curr_user_cnt | percentage_change |
| ------------------------ | ------------- | ------------------------ | ------------- | ----------------- |
| 2018-07-01T00:00:00.000Z | 5             | 2018-08-01T00:00:00.000Z | 2             | -60.00            |
| 2018-08-01T00:00:00.000Z | 2             | 2018-09-01T00:00:00.000Z | 1             | -50.00            |
| 2018-09-01T00:00:00.000Z | 1             | 2018-10-01T00:00:00.000Z | 1             | 0.00              |
| 2018-10-01T00:00:00.000Z | 1             | 2018-11-01T00:00:00.000Z | 3             | 200.00            |

---

[View on DB Fiddle](https://www.db-fiddle.com/f/f6bkBVHwHXAxvVdnCEcwcA/1)
