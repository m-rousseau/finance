-- Table: public.stocks

-- DROP TABLE IF EXISTS public.stocks;

CREATE TABLE IF NOT EXISTS public.stocks
(
    pk character varying(64) COLLATE pg_catalog."default" NOT NULL,
    ticker character varying(20) COLLATE pg_catalog."default" NOT NULL,
    open double precision NOT NULL,
    close double precision NOT NULL,
    low double precision NOT NULL,
    high double precision NOT NULL,
    vwap double precision NOT NULL,
    volume double precision NOT NULL,
    eodtimestamp bigint NOT NULL,
    date date NOT NULL,
    CONSTRAINT stocks_pkey PRIMARY KEY (pk)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.stocks
    OWNER to postgres;