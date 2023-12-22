-- Table: public.gov_debt_to_penny.sql

-- DROP TABLE IF EXISTS public.gov_debt_to_penny.sql;

CREATE TABLE IF NOT EXISTS public.gov_debt_to_penny
(
    record_date date NOT NULL,
    debt_held_public_amt double precision NOT NULL,
    intragov_hold_amt double precision NOT NULL,
    tot_pub_debt_out_amt double precision NOT NULL,
    CONSTRAINT gov_debt_to_penny_pkey PRIMARY KEY (record_date)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.gov_debt_to_penny
    OWNER to postgres;