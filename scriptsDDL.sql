CREATE SCHEMA music;
GO

CREATE TABLE music.usuarios(
    id_usuario int IDENTITY(1,1) PRIMARY KEY
    , nombre NVARCHAR(100) NOT NULL
    , email NVARCHAR(100) NOT NULL UNIQUE
    , fecha_registro DATETIME DEFAULT SYSDATETIME ()

)

