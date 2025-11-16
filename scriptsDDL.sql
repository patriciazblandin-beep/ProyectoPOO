
CREATE SCHEMA music;
GO

CREATE TABLE music.usuarios(
    id_usuario int IDENTITY(1,1) PRIMARY KEY
    , nombre NVARCHAR(100) NOT NULL
    , email NVARCHAR(100) NOT NULL UNIQUE
    , fecha_registro DATETIME DEFAULT SYSDATETIME ()

)
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

-- Verificar si el esquema 'music' existe
SELECT name FROM sys.schemas WHERE name = 'music';

---Tabla Artista
CREATE TABLE music.artistas(
    id_artista INT IDENTITY (1,1) PRIMARY KEY
    , nombre NVARCHAR(100) NOT NULL
    , discografica NVARCHAR(150)
)

--Tabla Albumes
CREATE TABLE music.albumes(
    id_album INT IDENTITY (1,1) PRIMARY KEY
    , id_artista INT NOT NULL
    , titulo NVARCHAR(150) NOT NULL
    , fecha_lanzamiento DATE    
)

ALTER TABLE music.albumes
ADD CONSTRAINT FK_albumes_artistas
FOREIGN KEY (id_artista) REFERENCES music.artistas(id_artista)

--Tabla Canciones---
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

ALTER TABLE music.playlists_canciones
ADD CONSTRAINT FK_playlistsCanciones_playlists
FOREIGN KEY (id_playlists) REFERENCES music.playlists(id_playlists)

ALTER TABLE music.playlists_canciones
ADD CONSTRAINT FK_playlistCanciones_canciones
FOREIGN KEY (id_cancion) REFERENCES music.canciones(id_cancion)