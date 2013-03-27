-- sample users
insert into Users values('sbchou', 'password');
insert into Users values('don8yu', 'password');
insert into Users values('don4yu', 'password');
insert into Users values('alice01', 'password');
insert into Users values('cleobc', 'password');
insert into Users values('caroline', 'password');
insert into Users values('sunnylinda', 'password');
insert into Users values('tricepat', 'password');
insert into Users values('stephzhou', 'password');
insert into Users values('cmoscardi', 'password');

insert into Emails values('sbchou@gmail.com', 1);
insert into Emails values('donyu8@gmail.com', 1);
insert into Emails values('xiaodonyu@gmail.com', 0);
insert into Emails values('alice@gmail.com', 0);
insert into Emails values('cleobc@gmail.com', 1);
insert into Emails values('laflutechantante@gmail.com', 1);
insert into Emails values('linda.z.sun@gmail.com', 1);
insert into Emails values('patrice@gmail.com', 0);
insert into Emails values('stephen@gmail.com', 1);
insert into Emails values('cmoscardi@gmail.com', 1);

insert into has values('sbchou', 'sbchou@gmail.com');
insert into has values('don8yu', 'donyu8@gmail.com');
insert into has values('don4yu', 'xiaodonyu@gmail.com');
insert into has values('alice01', 'alice@gmail.com');
insert into has values('cleobc', 'cleobc@gmail.com');
insert into has values('caroline', 'laflutechantante@gmail.com');
insert into has values('sunnylinda', 'linda.z.sun@gmail.com');
insert into has values('tricepat', 'patrice@gmail.com');
insert into has values('stephzhou', 'stephen@gmail.com');
insert into has values('cmoscardi', 'cmoscardi@gmail.com');

insert into friends_with values('sbchou', 'don8yu');
insert into friends_with values('sbchou', 'don4yu');   
insert into friends_with values('sbchou', 'alice01');
insert into friends_with values('sbchou', 'cleobc');
insert into friends_with values('sbchou', 'caroline');
insert into friends_with values('sbchou', 'sunnylinda');
insert into friends_with values('sbchou', 'tricepat');
insert into friends_with values('sbchou', 'stephzhou');
insert into friends_with values('sbchou', 'cmoscardi');
insert into friends_with values('don8yu', 'sbchou');

insert into SecurityQuestions values(1, 'what is your mothers maiden name', 'li', 'sbchou');
insert into SecurityQuestions values(2, 'what is your mothers maiden name', 'li', 'don8yu');
insert into SecurityQuestions values(3, 'what is your mothers maiden name', 'li', 'don4yu');
insert into SecurityQuestions values(4, 'what is your mothers maiden name', 'li', 'alice01');
insert into SecurityQuestions values(5, 'what is your mothers maiden name', 'li', 'cleobc');
insert into SecurityQuestions values(6, 'what is your mothers maiden name', 'li', 'caroline');
insert into SecurityQuestions values(7, 'what is your mothers maiden name', 'li', 'sunnylinda');
insert into SecurityQuestions values(8, 'what is your mothers maiden name', 'li', 'tricepat');
insert into SecurityQuestions values(9, 'what is your mothers maiden name', 'li', 'stephzhou');
insert into SecurityQuestions values(0, 'what is your mothers maiden name', 'li', 'cmoscardi');






























