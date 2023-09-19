CREATE TABLE public.daily_ticker
(
    id smallint NOT NULL,
    symbol character varying(8) COLLATE pg_catalog."default" NOT NULL,
    open double precision NOT NULL,
    close double precision NOT NULL,
    high double precision NOT NULL,
    low double precision NOT NULL,
    volume bigint NOT NULL,
    date date NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE public.daily_ticker
    OWNER to postgres;