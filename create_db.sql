-- Table: public.tickets

-- DROP TABLE public.tickets;

CREATE TABLE public.tickets
(
  id integer NOT NULL,
  status character varying(10) DEFAULT 'open',
  comments jsonb default '[]',
  CONSTRAINT tickets_pkey PRIMARY KEY (id),
  create_date timestamp default null,
  update_date timestamp default null,
  subject character varying(40),
  message text,
  email character varying(254)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.tickets
  OWNER TO postgres;
GRANT ALL ON TABLE public.tickets TO postgres;
GRANT ALL ON TABLE public.tickets TO ticket_user;
