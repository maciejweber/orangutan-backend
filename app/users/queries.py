GET_USERS = "SELECT id, email, is_active, insstmp, updstmp FROM users"
GET_USERS_EMAIL_AND_PASSWORD = "SELECT id, email FROM users WHERE email = $1 AND passwd = $2"
INSERT_USER = "INSERT into users (email, passwd, is_active) VALUES($1, $2, $3) RETURNING id, email"
GET_EXERCISES = "SELECT name FROM exercises"
