drop table if exists pizzaorder;
create table pizzaorder (
  orderId integer primary key autoincrement,
  piesize integer not null,
  premade text not null,
  toppings text,
  name text not null,
  phone text not null,
  message text
);

create table payment (
  orderId integer,
  creditcard integer,
  Month text,
  Year integer,
  seccode integer,
  zip integer
);
