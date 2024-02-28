
BEGIN;


CREATE TABLE IF NOT EXISTS public.captcha
(
    id integer NOT NULL DEFAULT nextval('captcha_id_seq'::regclass),
    text character varying(255) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT captcha_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.event
(
    event_id integer NOT NULL DEFAULT nextval('event_event_id_seq'::regclass),
    event_loc jsonb,
    sport integer,
    creator_id integer NOT NULL,
    event_date timestamp without time zone,
    type character(1) COLLATE pg_catalog."default",
    CONSTRAINT event_pkey PRIMARY KEY (event_id)
);

CREATE TABLE IF NOT EXISTS public.event_participants
(
    user_id integer NOT NULL,
    event_id integer NOT NULL,
    CONSTRAINT event_participants_pkey PRIMARY KEY (event_id, user_id)
);

CREATE TABLE IF NOT EXISTS public.event_point
(
    event_id integer NOT NULL DEFAULT nextval('event_event_id_seq'::regclass),
    event_loc jsonb,
    sport integer,
    creator_id integer NOT NULL,
    event_date timestamp without time zone,
    type character(1) COLLATE pg_catalog."default",
    event_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    info character varying(500) COLLATE pg_catalog."default",
    max_participants integer NOT NULL,
    duration numeric,
    difficulty character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT event_point_pkey PRIMARY KEY (event_id)
);

CREATE TABLE IF NOT EXISTS public.event_route
(
    event_id integer NOT NULL DEFAULT nextval('event_event_id_seq'::regclass),
    event_loc jsonb,
    sport integer,
    creator_id integer NOT NULL,
    event_date timestamp without time zone,
    type character(1) COLLATE pg_catalog."default",
    event_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    eventroute jsonb,
    info character varying(500) COLLATE pg_catalog."default",
    max_participants integer NOT NULL,
    duration numeric,
    difficulty character varying(100) COLLATE pg_catalog."default"
);

CREATE TABLE IF NOT EXISTS public.users
(
    user_id integer NOT NULL DEFAULT nextval('users_user_id_seq'::regclass),
    firstname character varying(255) COLLATE pg_catalog."default",
    surname character varying(255) COLLATE pg_catalog."default",
    username character varying(255) COLLATE pg_catalog."default",
    password character varying(500) COLLATE pg_catalog."default",
    birthdate date,
    email character varying(255) COLLATE pg_catalog."default",
    fav_sports character varying(255)[] COLLATE pg_catalog."default" NOT NULL DEFAULT '{}'::character varying[],
    gender character(1) COLLATE pg_catalog."default",
    postal_code character varying(10) COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (user_id)
);

ALTER TABLE IF EXISTS public.event
    ADD CONSTRAINT event_creator_id_fkey FOREIGN KEY (creator_id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.event_participants
    ADD CONSTRAINT user_event_point_event_id_fkey FOREIGN KEY (event_id)
    REFERENCES public.event_point (event_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.event_participants
    ADD CONSTRAINT user_event_point_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.event_point
    ADD CONSTRAINT event_point_creator_id_fkey FOREIGN KEY (creator_id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.event_route
    ADD CONSTRAINT event_route_creator_id_fkey FOREIGN KEY (creator_id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

CREATE OR REPLACE FUNCTION insert_event_point(
    p_event_loc JSONB,
    p_sport INT,
    p_creator_id INT,
    p_event_date TIMESTAMP,
    p_type CHAR(1),
    p_event_name VARCHAR(100),
    p_info VARCHAR(500),
    p_max_participants INT,
    p_duration decimal,
    p_difficulty VARCHAR(100)
) RETURNS VOID AS $$
BEGIN
    p_event_loc = p_event_loc::jsonb;
    INSERT INTO event_point (event_loc, sport, creator_id, event_date, type, event_name, info, max_participants, duration, difficulty)
    VALUES (
        p_event_loc,
        p_sport,
        p_creator_id,
        p_event_date,
        p_type,
        p_event_name,
        p_info,
        p_max_participants,
        p_duration,
        p_difficulty
    );


END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION trigger_event_point()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO event (event_loc, sport, creator_id, event_date, type,)
    VALUES (NEW.event_loc, NEW.sport, NEW.creator_id ,NEW.event_date, 'p',);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER before_insert_event_point
BEFORE INSERT ON event_point
FOR EACH ROW EXECUTE FUNCTION trigger_event_point();


CREATE OR REPLACE FUNCTION trigger_event_route()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO event (event_loc, sport, creator_id, event_date, type)
    VALUES (NEW.event_loc, NEW.sport, NEW.creator_id ,NEW.event_date, 'r')
    RETURNING event_id INTO NEW.event_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER before_insert_event_route
BEFORE INSERT ON event_route
FOR EACH ROW EXECUTE FUNCTION trigger_event_point();

END;