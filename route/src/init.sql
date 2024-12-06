CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS public.trayecto
(
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    "flightId" character varying COLLATE pg_catalog."default",
    "sourceAirportCode" character varying(3) COLLATE pg_catalog."default",
    "sourceCountry" character varying COLLATE pg_catalog."default",
    "destinyAirportCode" character varying(3) COLLATE pg_catalog."default",
    "destinyCountry" character varying COLLATE pg_catalog."default",
    "bagCost" integer,
    "plannedStartDate" timestamp with time zone,
    "plannedEndDate" timestamp with time zone,
    "createdAt" timestamp with time zone,
    "updateAt" timestamp with time zone
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.trayecto
    OWNER to postgres;