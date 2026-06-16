import 'dotenv/config';

export default {
  schema: './src/modules/*/*.models.js',
  out: './drizzle',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL,
  },
};
