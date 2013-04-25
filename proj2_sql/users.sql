-- sample users
insert into Users values('sbchou', 'password', profile_image(1, 'this is my face', 'img/profpic1.jpg', 'sbchou', 'img/thumbnail1.jpg'));
insert into Users values('don8yu', 'password', profile_image(2, 'this is my face', 'img/profpic2.jpg', 'don8yu', 'img/thumbnail2.jpg'));
insert into Users values('don4yu', 'password', profile_image(3, 'this is my face', 'img/profpic3.jpg', 'don4yu', 'img/thumbnail3.jpg'));
insert into Users values('alice01', 'password', profile_image(4, 'this is my face', 'img/profpic4.jpg', 'alice01', 'img/thumbnail4.jpg'));
insert into Users values('cleobc', 'password', profile_image(5, 'this is my face', 'img/profpic5.jpg', 'cleobc', 'img/thumbnail5.jpg'));
insert into Users values('caroline', 'password', profile_image(6, 'this is my face', 'img/profpic6.jpg', 'caroline', 'img/thumbnail6.jpg'));
insert into Users values('sunnylinda', 'password', profile_image(7, 'this is my face', 'img/profpic7.jpg', 'sunnylinda', 'img/thumbnail7.jpg'));
insert into Users values('tricepat', 'password', profile_image(8, 'this is my face', 'img/profpic8.jpg', 'tricepat', 'img/thumbnail8.jpg'));
insert into Users values('stephzhou', 'password', profile_image(9, 'this is my face', 'img/profpic9.jpg', 'stephzhou', 'img/thumbnail9.jpg'));
insert into Users values('cmoscardi', 'password', profile_image(10, 'this is my face', 'img/profpic10.jpg', 'cmoscardi', 'img/thumbnail10.jpg'));

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






























