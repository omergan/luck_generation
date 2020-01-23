BEGIN TRANSACTION;
DROP TABLE IF EXISTS "users";
CREATE TABLE IF NOT EXISTS "users" (
	"id"	integer NOT NULL,
	"id_str"	text NOT NULL,
	"name"	text,
	"username"	text NOT NULL,
	"bio"	text,
	"location"	text,
	"url"	text,
	"join_date"	text NOT NULL,
	"join_time"	text NOT NULL,
	"tweets"	integer,
	"following"	integer,
	"followers"	integer,
	"likes"	integer,
	"media"	integer,
	"private"	integer NOT NULL,
	"verified"	integer NOT NULL,
	"profile_image_url"	text NOT NULL,
	"background_image"	text,
	"hex_dig"	text NOT NULL,
	"time_update"	integer NOT NULL,
	CONSTRAINT "users_pk" PRIMARY KEY("id","hex_dig")
);
DROP TABLE IF EXISTS "tweets";
CREATE TABLE IF NOT EXISTS "tweets" (
	"id"	integer NOT NULL,
	"id_str"	text NOT NULL,
	"tweet"	text DEFAULT '',
	"conversation_id"	text NOT NULL,
	"created_at"	integer NOT NULL,
	"date"	text NOT NULL,
	"time"	text NOT NULL,
	"timezone"	text NOT NULL,
	"place"	text DEFAULT '',
	"replies_count"	integer,
	"likes_count"	integer,
	"retweets_count"	integer,
	"user_id"	integer NOT NULL,
	"user_id_str"	text NOT NULL,
	"screen_name"	text NOT NULL,
	"name"	text DEFAULT '',
	"link"	text,
	"mentions"	text,
	"hashtags"	text,
	"cashtags"	text,
	"urls"	text,
	"photos"	text,
	"quote_url"	text,
	"video"	integer,
	"geo"	text,
	"near"	text,
	"source"	text,
	"time_update"	integer NOT NULL,
	"translate"	text DEFAULT '',
	"trans_src"	text DEFAULT '',
	"trans_dest"	text DEFAULT '',
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "retweets";
CREATE TABLE IF NOT EXISTS "retweets" (
	"user_id"	integer NOT NULL,
	"username"	text NOT NULL,
	"tweet_id"	integer NOT NULL,
	"retweet_id"	integer NOT NULL,
	"retweet_date"	integer NOT NULL,
	CONSTRAINT "retweets_pk" PRIMARY KEY("user_id","tweet_id"),
	CONSTRAINT "user_id_fk" FOREIGN KEY("user_id") REFERENCES "users"("id"),
	CONSTRAINT "tweet_id_fk" FOREIGN KEY("tweet_id") REFERENCES "tweets"("id")
);
DROP TABLE IF EXISTS "replies";
CREATE TABLE IF NOT EXISTS "replies" (
	"tweet_id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"username"	text NOT NULL,
	CONSTRAINT "replies_pk" PRIMARY KEY("user_id","tweet_id"),
	CONSTRAINT "tweet_id_fk" FOREIGN KEY("tweet_id") REFERENCES "tweets"("id")
);
DROP TABLE IF EXISTS "favorites";
CREATE TABLE IF NOT EXISTS "favorites" (
	"user_id"	integer NOT NULL,
	"tweet_id"	integer NOT NULL,
	CONSTRAINT "user_id_fk" FOREIGN KEY("user_id") REFERENCES "users"("id"),
	CONSTRAINT "favorites_pk" PRIMARY KEY("user_id","tweet_id"),
	CONSTRAINT "tweet_id_fk" FOREIGN KEY("tweet_id") REFERENCES "tweets"("id")
);
DROP TABLE IF EXISTS "followers";
CREATE TABLE IF NOT EXISTS "followers" (
	"id"	integer NOT NULL,
	"follower_id"	integer NOT NULL,
	CONSTRAINT "id_fk" FOREIGN KEY("id") REFERENCES "users"("id"),
	CONSTRAINT "follower_id_fk" FOREIGN KEY("follower_id") REFERENCES "users"("id"),
	CONSTRAINT "followers_pk" PRIMARY KEY("id","follower_id")
);
DROP TABLE IF EXISTS "following";
CREATE TABLE IF NOT EXISTS "following" (
	"id"	integer NOT NULL,
	"following_id"	integer NOT NULL,
	CONSTRAINT "id_fk" FOREIGN KEY("id") REFERENCES "users"("id"),
	CONSTRAINT "following_id_fk" FOREIGN KEY("following_id") REFERENCES "users"("id"),
	CONSTRAINT "following_pk" PRIMARY KEY("id","following_id")
);
DROP TABLE IF EXISTS "followers_names";
CREATE TABLE IF NOT EXISTS "followers_names" (
	"user"	text NOT NULL,
	"time_update"	integer NOT NULL,
	"follower"	text NOT NULL,
	PRIMARY KEY("user","follower")
);
DROP TABLE IF EXISTS "following_names";
CREATE TABLE IF NOT EXISTS "following_names" (
	"user"	text NOT NULL,
	"time_update"	integer NOT NULL,
	"follows"	text NOT NULL,
	PRIMARY KEY("user","follows")
);
COMMIT;
