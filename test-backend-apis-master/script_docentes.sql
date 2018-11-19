-- Table: public.docente

-- DROP TABLE public.docente;

CREATE TABLE public.docente
(
  id integer NOT NULL DEFAULT nextval('docente_id_seq'::regclass),
  cedula character varying(100) NOT NULL,
  nombre character varying(100) NOT NULL,
  apellido character varying(100) NOT NULL,
  correo character varying(100) NOT NULL,
  grado character varying(50) NOT NULL,
  area_trabajo character varying(100) NOT NULL,
  sexo character varying(50) NOT NULL,
  num_citaciones integer NOT NULL,
  id_escalafon integer NOT NULL,
  fecha_creacion timestamp with time zone NOT NULL DEFAULT now(),
  fecha_actualizacion timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT id_docente PRIMARY KEY (id),
  CONSTRAINT id_escalafon FOREIGN KEY (id_escalafon)
      REFERENCES public.escalon (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT docente_cedula_key UNIQUE (cedula)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.docente
  OWNER TO postgres;

-- Index: public.fki_id_escalafon

-- DROP INDEX public.fki_id_escalafon;

CREATE INDEX fki_id_escalafon
  ON public.docente
  USING btree
  (id_escalafon);


INSERT INTO public.docente(
            cedula, nombre, apellido, correo, grado, area_trabajo, sexo, 
            num_citaciones, id_escalafon)
    VALUES ('11356034', 'Mirella', 'Herrera', 'mirella.herrera@gmail.com', 'doctorado', 'investigacion', 'Femenino', 123, 5);


INSERT INTO public.docente(
            cedula, nombre, apellido, correo, grado, area_trabajo, sexo, 
            num_citaciones, id_escalafon)
    VALUES ('1515515', 'Dessiree', 'Delgado', 'desidelgado@gmail.com', 'doctorado', 'investigacion', 'Femenino', 563, 5);


INSERT INTO public.docente(
            cedula, nombre, apellido, correo, grado, area_trabajo, sexo, 
            num_citaciones, id_escalafon)
    VALUES ('545511', 'Marilyn', 'Guigni', 'marilyngiugni@gmail.com', 'maestria y especializacion', 'investigacion', 'Femenino', 232, 5);


-- Table: public.escalon

-- DROP TABLE public.escalon;

CREATE TABLE public.escalon
(
  id integer NOT NULL DEFAULT nextval('escalon_id_seq'::regclass),
  nombre character varying NOT NULL,
  fecha_creacion timestamp with time zone NOT NULL DEFAULT now(),
  fecha_actualizacion timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT escalon_pkey PRIMARY KEY (id),
  CONSTRAINT escalon_nombre_key UNIQUE (nombre)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.escalon
  OWNER TO postgres;


INSERT INTO public.escalon(
            nombre)
    VALUES ('Instructor');

INSERT INTO public.escalon(
            nombre)
    VALUES ('Asistente');

INSERT INTO public.escalon(
            nombre)
    VALUES ('Agregado');

INSERT INTO public.escalon(
            nombre)
    VALUES ('Asociado');

INSERT INTO public.escalon(
            nombre)
    VALUES ('Titular');

-- Table: public.otro_estudio

-- DROP TABLE public.otro_estudio;

CREATE TABLE public.otro_estudio
(
  descripcion character varying(100) NOT NULL,
  institucion character varying(100) NOT NULL,
  id integer NOT NULL DEFAULT nextval('otro_estudio_id_seq'::regclass),
  fecha_creacion timestamp with time zone NOT NULL DEFAULT now(),
  fecha_actualizacion timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT otro_estudio_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.otro_estudio
  OWNER TO postgres;


INSERT INTO public.otro_estudio(
            descripcion, institucion)
    VALUES ('Estudio1', 'Universidad de Carabobo');

INSERT INTO public.otro_estudio(
            descripcion, institucion)
    VALUES ('Estudio2', 'Universidad de los Andes');

INSERT INTO public.otro_estudio(
            descripcion, institucion)
    VALUES ('Estudio3', 'CEFORCOM');

INSERT INTO public.otro_estudio(
            descripcion, institucion)
    VALUES ('Estudio4', 'Universidad de Chile');


-- Table: public.premio

-- DROP TABLE public.premio;

CREATE TABLE public.premio
(
  id integer NOT NULL DEFAULT nextval('premio_id_seq'::regclass),
  nombre_premio character varying(100) NOT NULL,
  institucion character varying(100) NOT NULL,
  fecha_creacion timestamp with time zone NOT NULL DEFAULT now(),
  fecha_actualizacion timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT premio_pkey PRIMARY KEY (id),
  CONSTRAINT premio_nombre_premio_key UNIQUE (nombre_premio)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.premio
  OWNER TO postgres;

INSERT INTO public.premio(
            nombre_premio, institucion)
    VALUES ('Mejor profesor', 'Universidad de Carabobo');

INSERT INTO public.premio(
            nombre_premio, institucion)
    VALUES ('Mejor Investigador 2016', 'Universidad de Carabobo');

INSERT INTO public.premio(
            nombre_premio, institucion)
    VALUES ('Mejor publicacion 2018', 'Universidad de los Andes');

INSERT INTO public.premio(
            nombre_premio, institucion)
    VALUES ('Mejor publicacion 2019', 'Universidad de los Carabobo');


-- Table: public.proyecto

-- DROP TABLE public.proyecto;

CREATE TABLE public.proyecto
(
  id integer NOT NULL DEFAULT nextval('proyecto_id_seq'::regclass),
  titulo character varying(100) NOT NULL,
  tipo character varying(50) NOT NULL,
  fecha_creacion timestamp with time zone NOT NULL DEFAULT now(),
  fecha_actualizacion timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT proyecto_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.proyecto
  OWNER TO postgres;


INSERT INTO public.proyecto(
            titulo, tipo)
    VALUES ('Proyecto1', 'Investigacion');

INSERT INTO public.proyecto(
            titulo, tipo)
    VALUES ('Proyecto2', 'Publicacion');

INSERT INTO public.proyecto(
            titulo, tipo)
    VALUES ('Proyecto3', 'Publicacion');

INSERT INTO public.proyecto(
            titulo, tipo)
    VALUES ('Proyecto4', 'Otro tipo');

-- Table: public.publicacion

-- DROP TABLE public.publicacion;

CREATE TABLE public.publicacion
(
  id integer NOT NULL DEFAULT nextval('publicacion_id_seq'::regclass),
  tipo character varying(50) NOT NULL,
  autor character varying(100) NOT NULL,
  titulo character varying(100) NOT NULL,
  fecha date NOT NULL,
  revista character varying(100) NOT NULL,
  fecha_creacion timestamp with time zone NOT NULL DEFAULT now(),
  fecha_actualizacion timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT publicacion_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.publicacion
  OWNER TO postgres;


INSERT INTO public.publicacion(
            tipo, autor, titulo, fecha, revista)
    VALUES ('Tipo1', 'Mirella Herrera', 'Titulo de la publicacion1', '2012-05-30', 'Revista Cientifica');


INSERT INTO public.publicacion(
            tipo, autor, titulo, fecha, revista)
    VALUES ('Tipo1', 'Desiree Delgado, Mirella Herrera', 'Titulo de la publicacion2', '2013-08-30', 'Revista Cientifica2');

INSERT INTO public.publicacion(
            tipo, autor, titulo, fecha, revista)
    VALUES ('Tipo2', 'Desiree Delgado', 'Titulo de la publicacion3', '2014-10-10', 'Revista Cientifica');


-- Table: public.citacion

-- DROP TABLE public.citacion;

CREATE TABLE public.citacion
(
  id integer NOT NULL DEFAULT nextval('citacion_id_seq'::regclass),
  trabajo_donde_donde_se_cita character varying(100),
  fecha_creacion timestamp with time zone NOT NULL DEFAULT now(),
  fecha_actualizacion timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT citacion_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.citacion
  OWNER TO postgres;



INSERT INTO public.citacion(
            trabajo_donde_donde_se_cita)
    VALUES ('Trabajo1');


INSERT INTO public.citacion(
            trabajo_donde_donde_se_cita)
    VALUES ('Trabajo2');

INSERT INTO public.citacion(
            trabajo_donde_donde_se_cita)
    VALUES ('Trabajo3');

INSERT INTO public.citacion(
            trabajo_donde_donde_se_cita)
    VALUES ('Trabajo4');

-- Table: public.titulo

-- DROP TABLE public.titulo;

CREATE TABLE public.titulo
(
  id integer NOT NULL DEFAULT nextval('titulo_id_seq'::regclass),
  tipo character varying(50) NOT NULL,
  descripcion character varying(100) NOT NULL,
  nivel character varying(50) NOT NULL,
  universidad character varying(100) NOT NULL,
  fecha_creacion timestamp with time zone NOT NULL DEFAULT now(),
  fecha_actualizacion timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT titulo_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.titulo
  OWNER TO postgres;

INSERT INTO public.titulo(
            tipo, descripcion, nivel, universidad)
    VALUES ('Licenciado', 'Licenciado en Computacion','nivel', 'Universidad de Carabobo');

INSERT INTO public.titulo(
            tipo, descripcion, nivel, universidad)
    VALUES ('Ingeniero', 'Ingeniero de Sistemas','nivel', 'Universidad de Carabobo');

--RELACIONES

INSERT INTO public.docente_facultad(
           id_facultad, id_docente)
    VALUES (2, 1);


INSERT INTO public.docente_facultad(
           id_facultad, id_docente)
    VALUES (2, 2);

INSERT INTO public.docente_facultad(
           id_facultad, id_docente)
    VALUES (3, 3);




INSERT INTO public.docente_otro_estudio(
            id_docente, id_otro_estudio)
    VALUES (1, 1);

INSERT INTO public.docente_otro_estudio(
            id_docente, id_otro_estudio)
    VALUES (1, 4);

INSERT INTO public.docente_otro_estudio(
            id_docente, id_otro_estudio)
    VALUES (2, 2);

INSERT INTO public.docente_otro_estudio(
            id_docente, id_otro_estudio)
    VALUES (2, 3);


INSERT INTO public.docente_otro_estudio(
            id_docente, id_otro_estudio)
    VALUES (3, 1);


INSERT INTO public.docente_otro_estudio(
            id_docente, id_otro_estudio)
    VALUES (3, 2);

INSERT INTO public.docente_otro_estudio(
            id_docente, id_otro_estudio)
    VALUES (3, 4);


INSERT INTO public.docente_premio(
            id_docente, id_premio)
    VALUES (1, 1);

INSERT INTO public.docente_premio(
            id_docente, id_premio)
    VALUES (1, 4);

INSERT INTO public.docente_premio(
            id_docente, id_premio)
    VALUES (3, 2);


INSERT INTO public.docente_proyecto(
            id_docente, id_proyecto)
    VALUES (2, 2);

INSERT INTO public.docente_proyecto(
            id_docente, id_proyecto)
    VALUES (1, 2);


INSERT INTO public.docente_proyecto(
            id_docente, id_proyecto)
    VALUES (3, 4);

INSERT INTO public.docente_proyecto(
            id_docente, id_proyecto)
    VALUES (3, 3);


INSERT INTO public.docente_publicacion(
            id_docente, id_publicacion)
    VALUES (1, 2);

INSERT INTO public.docente_publicacion(
            id_docente, id_publicacion)
    VALUES (2, 2);


INSERT INTO public.docente_publicacion(
            id_docente, id_publicacion)
    VALUES (1, 1);

INSERT INTO public.docente_publicacion(
            id_docente, id_publicacion)
    VALUES (2, 3);

INSERT INTO public.publicacion_citacion(
            id_publicacion, id_citacion)
    VALUES (1, 1);


INSERT INTO public.publicacion_citacion(
            id_publicacion, id_citacion)
    VALUES (1, 4);

INSERT INTO public.publicacion_citacion(
            id_publicacion, id_citacion)
    VALUES (2, 3);

INSERT INTO public.publicacion_citacion(
            id_publicacion, id_citacion)
    VALUES (2, 1);

INSERT INTO public.publicacion_citacion(
            id_publicacion, id_citacion)
    VALUES (3, 3);

INSERT INTO public.docente_titulo(
            id_docente, id_titulo)
    VALUES (1, 2);

INSERT INTO public.docente_titulo(
            id_docente, id_titulo)
    VALUES (2, 1);
    
INSERT INTO public.docente_titulo(
            id_docente, id_titulo)
    VALUES (2, 2);

INSERT INTO public.docente_titulo(
            id_docente, id_titulo)
    VALUES (3, 1);

