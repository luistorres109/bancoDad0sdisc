create table projeto ( projeto_id   number primary key 
                     , nome         varchar2(100)
                     , data_entrega date not null
                     , tipo         varchar2(100)
                     , produto      varchar2(100)
                     );
                     
create table pessoa( pessoa_id  number primary key
                   , nome       varchar2(100) not null 
                   , cpf        varchar2(14) not null
                   , numero     varchar2(12) not null
                   , email      varchar2(100) not null
                   , endereco   varchar2(100) not null
                   , projeto_id number not null
                   );
                   
create table equipe ( equipe_id number primary key
                    , nome    varchar2(100)
                    , projeto_id number not null
                    );
                  
                  
alter table pessoa add constraint fk_projeto_pessoa foreign key (projeto_id) references projeto(projeto_id);

alter table equipe add constraint fk_projeto_equipe foreign key (projeto_id) references projeto(projeto_id);

create sequence pesoa;

create sequence projeto_id;
--
insert into pessoa values(1, 'teste', '123.456.789-00', '4999999-9999', 'eduardo@hotmail.com', 'rua teste, bairro teste, numero 12', 1);

insert into pessoa values (pesoa.nextval, 'Eduardo', '123.456.789-00', '4991234-5678', 'eduardo@hotmail.com', 'rua teste, bairro teste, numero 12', 1);
insert into pessoa values (pesoa.nextval, 'henrique', '123.456.789-00', '4991234-5678', 'henrique@hotmail.com', 'rua teste1, bairro teste, numero 19', 1);
insert into pessoa values (pesoa.nextval, 'Ruam', '123.456.789-00', '4991234-5678', 'Ruam@hotmail.com', 'rua teste2, bairro teste, numero 29', 1);
insert into pessoa values (pesoa.nextval, 'Geio', '123.456.789-00', '4991234-5678', 'Geio@hotmail.com', 'rua teste3, bairro teste, numero 39', 1);
insert into pessoa values (pesoa.nextval, 'Gerson', '123.456.789-00', '4991234-5678', 'Gerson@hotmail.com', 'rua teste4, bairro teste, numero 49', 2);
insert into pessoa values (pesoa.nextval, 'Monica', '123.456.789-00', '4991234-5678', 'Monica@hotmail.com', 'rua teste5, bairro teste, numero 59', 2);
insert into pessoa values (pesoa.nextval, 'Radames', '123.456.789-00', '4991234-5678', 'Radames@hotmail.com', 'rua teste6, bairro teste, numero 69', 2);
insert into pessoa values (pesoa.nextval, 'teste', '123.456.789-00', '4991234-5678', 'teste@hotmail.com', 'rua teste7, bairro teste, numero 79', 2);

insert into pessoa (pessoa_id, nome, cpf, numero, email, endereco ) values (&pessoa_id, &nome, &cpf, &numero, &email, &endereco);

select * from pessoa

--

insert into projeto values (1, 'projeto A', sysdate, 'projeto banco de dados', 'software');
insert into projeto values (2, 'projeto B', sysdate, 'analise', 'projeto');

select * from projeto

delete from projeto where projeto_id = 1;

update pessoa set
pessoa_id = 37
where pessoa_id = 1
--

select * 
from pessoa a
   , projeto b
   where a.projeto_id = b.projeto_id
   and b.projeto_id = 2


--
insert into equipe values ( 1, 'time A', 1);
insert into equipe values ( 2, 'time B', 2);

select *
  from pessoa  pes
     , projeto pro
     , equipe  equ
 where pes.projeto_id = pro.projeto_id
   and equ.projeto_id = pro.projeto_id
   and pro.projeto_id = 1;
--
select *
  from pessoa  pes
     , projeto pro
     , equipe  equ
 where pes.projeto_id = pro.projeto_id
   and equ.projeto_id = pro.projeto_id
   and pro.projeto_id = 2;
   
--



