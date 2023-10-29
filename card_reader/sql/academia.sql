CREATE TABLE clientes (
	codigo VARCHAR(8) PRIMARY KEY,
	nome VARCHAR(50)
);

INSERT INTO clientes VALUES
	('fabe1ebe', 'João da Silva'),
	('09b1cc28', 'Maria dos Santos'),
	('ac5aba32', 'Helena da Silva Lima'),
	('1b9052c3', 'José dos Reis');

CREATE TABLE mensalidades(
	cod_cliente VARCHAR(8),
	mes INT,
	situacao BOOLEAN default false,
	FOREIGN KEY(cod_cliente) REFERENCES  clientes(codigo)
);

INSERT INTO mensalidades VALUES
	('fabe1ebe', 1, true);
	
SELECT * FROM mensalidades;
