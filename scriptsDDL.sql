
CREATE SCHEMA music;
GO

CREATE TABLE music.usuarios(
    id_usuario int IDENTITY(1,1) PRIMARY KEY
    , nombre NVARCHAR(100) NOT NULL
    , email NVARCHAR(100) NOT NULL UNIQUE
    , fecha_registro DATETIME DEFAULT SYSDATETIME ()

)

SELECT * FROM music.usuarios  

--Tabla de playlist--
CREATE TABLE music.playlists(
    id_playlists INT IDENTITY(1,1) PRIMARY KEY
     , id_usuario INT NOT NULL
    , nombre NVARCHAR(200) NOT NULL
    , fecha_creacion DATETIME DEFAULT SYSDATETIME()
)

ALTER TABLE music.playlists 
ADD CONSTRAINT FK_playlists_usuarios
FOREIGN KEY (id_usuario) REFERENCES music.usuarios(id_usuario)

SELECT * FROM music.playlists 

---para verificar
SELECT name FROM sys.schemas WHERE name = 'music';
SELECT * FROM music.artistas

SELECT * FROM music.artistas 
---Tabla de los artitas
CREATE TABLE music.artistas(
    id_artista INT IDENTITY (1,1) PRIMARY KEY
    , nombre NVARCHAR(100) NOT NULL
    , discografica NVARCHAR(150)
)

--Tabla de albumes---
CREATE TABLE music.albumes(
    id_album INT IDENTITY (1,1) PRIMARY KEY
    , id_artista INT NOT NULL
    , titulo NVARCHAR(150) NOT NULL
    , fecha_lanzamiento DATE    
)

ALTER TABLE music.albumes
ADD CONSTRAINT FK_albumes_artistas
FOREIGN KEY (id_artista) REFERENCES music.artistas(id_artista)

SELECT * FROM music.albumes

--Tabla cancioness--
CREATE TABLE music.canciones(
    id_cancion INT IDENTITY(1,1) PRIMARY KEY 
    , id_album INT NOT NULL 
    , titulo NVARCHAR (150) NOT NULL
    , duracion TIME
    
)

ALTER TABLE music.canciones 
ADD CONSTRAINT FK_canciones_albumes
FOREIGN KEY (id_album) REFERENCES music.albumes(id_album)

DROP TABLE music.canciones;

CREATE TABLE music.playlists_canciones(
    id_playlists INT NOT NULL 
    , id_cancion INT NOT NULL 
    , comentario NVARCHAR(200)
     PRIMARY KEY (id_playlists , id_cancion) 
)
SELECT * FROM music.canciones

ALTER TABLE music.playlists_canciones
ADD CONSTRAINT FK_playlistsCanciones_playlists
FOREIGN KEY (id_playlists) REFERENCES music.playlists(id_playlists)

ALTER TABLE music.playlists_canciones
ADD CONSTRAINT FK_playlistCanciones_canciones
FOREIGN KEY (id_cancion) REFERENCES music.canciones(id_cancion)