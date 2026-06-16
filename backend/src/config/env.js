import dotenv from 'dotenv';

dotenv.config();

export const env = {
  port: process.env.PORT || 3000,

  dbHost: process.env.DB_HOST,
  dbPort: process.env.DB_PORT,
  dbName: process.env.DB_NAME,
  dbUser: process.env.DB_USER,
  dbPassword: process.env.DB_PASSWORD,

  jwtSecret: process.env.JWT_SECRET,
};
