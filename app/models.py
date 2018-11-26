from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

ACCESS = {
  'user': 0,
  'admin': 1
}

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(UserMixin, db.Model):

  __tablename__='users'

  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(255))
  email = db.Column(db.String(255))
  joined=db.Column(db.DateTime,default=datetime.now)
  first_name = db.Column(db.String(255))
  surname = db.Column(db.String(255))
  pass_secure = db.Column(db.String(255))
  access=db.Column(db.String(255), default=ACCESS['user'])

  comments = db.relationship('Comments', backref='user', lazy='dynamic')

  @property
  def password(self):
    raise AttributeError('You do not have the permissions to access this')

  @password.setter
  def password(self, password):
    self.pass_secure = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.pass_secure, password)

  def save_user(self):
    db.session.add(self)
    db.session.commit()

  def find_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user

  def is_admin(self):
    return self.access == ACCESS['admin']
    
  def allowed(self, access_level):
    return self.access >= access_level

  def init_db():
    if User.query.count() == 0:
      master = User(username='master', password='master', first_name='Jeremy', surname='Kimotho', email='projectsjeremy1000@gmail.com', access=ACCESS['admin'])
      
      db.session.add(master)
      db.session.commit()

  def __repr__(self):
    return f'User {self.username}'

class Comments(db.Model):
  __tablename__='comments'

  id = db.Column(db.Integer, primary_key = True)
  comment = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  posted = db.Column(db.DateTime,default=datetime.now)
  post = db.Column(db.Integer, db.ForeignKey('posts.id'))

  def save_comment(self):
    db.session.add(self)
    db.session.commit()

  def delete_comments(self):
    db.session.delete(self)
    db.session.commit()


  @classmethod
  def get_comments(cls, id):
    comments = Comments.query.filter_by(posted=id).all()
    return comments

class Post(db.Model):
  __tablename__='posts'

  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(255))
  body = db.Column(db.String)
  posted = db.Column(db.DateTime,default=datetime.utcnow)
  
  comments = db.relationship('Comments', backref='post_comments', lazy='dynamic')

  def save_post(self):
    db.session.add(self)
    db.session.commit()

  def delete_post(self):
    db.session.delete(self)
    db.session.commit()

  def get_specific_post(id):
    post = Post.query.filter_by(id=id).first()
    return post

  @classmethod
  def get_posts(cls):
    posts = Post.query.all()
    return posts

  def get_comments(self):
    post = Post.query.filter_by(id = self.id).first()
    comments = Comments.query.filter_by(post=post.id)
    return comments

  def default_posts():
    if Post.query.count() == 0:
      post1=Post(title='Let\'s talk Behavioral Psychology?', body="Let's define behavioral psychology. Behavioral psychology is the study of the connection between our minds and our behavior. Sometimes you will hear behavioral psychology referred to as behaviorism. The researchers and scientists who study behavioral psychology are trying to understand why we behave the way we do and they are concerned with discovering patterns in our actions and behaviors. The hope is that if we can use behavioral psychology to help us predict how humans will behave, we can build better habits as individuals, create better products as companies, and develop better living spaces as communities.")
      post2=Post(title='Motivation?', body="So what is motivation, exactly? The author Steven Pressfield has a great line in his book, The War of Art, which I think gets at the core of motivation. To paraphrase Pressfield, 'At some point, the pain of not doing it becomes greater than the pain of doing it.' In other words, at some point, it is easier to change than to stay the same. It is easier to take action and feel insecure at the gym than to sit still and experience self-loathing on the couch. It is easier to feel awkward while making the sales call than to feel disappointed about your dwindling bank account. This, I think, is the essence of motivation. Every choice has a price, but when we are motivated, it is easier to bear the inconvenience of action than the pain of remaining the same. Somehow we cross a mental threshold—usually after weeks of procrastination and in the face of an impending deadline—and it becomes more painful to not do the work than to actually do it.")
      post3=Post(title='What is Procrastination?', body="Human beings have been procrastinating for centuries. The problem is so timeless, in fact, that ancient Greek philosophers like Socrates and Aristotle developed a word to describe this type of behavior: Akrasia. Akrasia is the state of acting against your better judgment. It is when you do one thing even though you know you should do something else. Loosely translated, you could say that akrasia is procrastination or a lack of self-control.' Ok, definitions are great and all, but why do we procrastinate? What is going on in the brain that causes us to avoid the things we know we should be doing? This is a good time to bring some science into our discussion. Behavioral psychology research has revealed a phenomenon called “time inconsistency,” which helps explain why procrastination seems to pull us in despite our good intentions. Time inconsistency refers to the tendency of the human brain to value immediate rewards more highly than future rewards. The best way to understand this is by imagining that you have two selves: your Present Self and your Future Self. When you set goals for yourself — like losing weight or writing a book or learning a language — you are actually making plans for your Future Self. You are envisioning what you want your life to be like in the future. Researchers have found that when you think about your Future Self, it is quite easy for your brain to see the value in taking actions with long-term benefits. The Future Self values long-term rewards. However, while the Future Self can set goals, only the Present Self can take action. When the time comes to make a decision, you are no longer making a choice for your Future Self. Now you are in the present moment, and your brain is thinking about the Present Self. Researchers have discovered that the Present Self really likes instant gratification, not long-term payoff. So, the Present Self and the Future Self are often at odds with one another. The Future Self wants to be trim and fit, but the Present Self wants a donut. Sure, everyone knows you should eat healthy today to avoid being overweight in 10 years. But consequences like an increased risk for diabetes or heart failure are years away. Similarly, many young people know that saving for retirement in their 20s and 30s is crucial, but the benefit of doing so is decades off. It is far easier for the Present Self to see the value in buying a new pair of shoes than in socking away $100 for 70-year-old you. (If you're curious, there are some very good evolutionary reasons for why our brain values immediate rewards more highly than long-term rewards.) This is one reason why you might go to bed feeling motivated to make a change in your life, but when you wake up you find yourself falling back into old patterns. Your brain values long-term benefits when they are in the future (tomorrow), but it values immediate gratification when it comes to the present moment (today).")
      post4=Post(title='Creativity', body="The creative process is the act of making new connections between old ideas or recognizing relationships between concepts. Creative thinking is not about generating something new from a blank slate, but rather about taking what is already present and combining those bits and pieces in a way that has not been done previously. While being creative isn't easy, nearly all great ideas follow a similar creative process. In 1940, an advertising executive named James Webb Young published a short guide titled, A Technique for Producing Ideas. Young believed the process of creative connection always occurred in five steps. The Creative Process. Step 1: Gather new material. At first, you learn. During this stage you focus on 1) learning specific material directly related to your task and 2) learning general material by becoming fascinated with a wide range of concepts. Step 2: Thoroughly work over the materials in your mind. During this stage, you examine what you have learned by looking at the facts from different angles and experimenting with fitting various ideas together. Step 3: Step away from the problem. Next, you put the problem completely out of your mind and go do something else that excites you and energizes you. Step 4: Let your idea return to you. At some point, but only after you have stopped thinking about it, your idea will come back to you with a flash of insight and renewed energy. Step 5: Shape and develop your idea based on feedback. For any idea to succeed, you must release it out into the world, submit it to criticism, and adapt it as needed. While we often think of creativity as an event or as a natural skill that some people have and some don't, research  actually suggests that both creativity and non-creativity are learned. According to psychology professor Barbara Kerr, “approximately 22 percent of the variance [in creativity] is due to the influence of genes.” This discovery was made by studying the differences in creative thinking between sets of twins. All of this to say, claiming that “I'm just not the creative type” is a pretty weak excuse for avoiding creative thinking. Certainly, some people are primed to be more creative than others. However, nearly every person is born with some level of creative skill and the majority of our creative thinking abilities are trainable.")
      post5=Post(title='How to Make Smart Decisions and Avoid Bad Ones', body="Decision making is just what it sounds like: the action or process of making decisions. Sometimes we make logical decisions, but there are many times when we make emotional, irrational, and confusing choices. This page covers why we make poor decisions and discusses useful frameworks to expand your decision-making toolbox. I like to think of myself as a rational person, but I’m not one. The good news is it’s not just me — or you. We are all irrational. For a long time, researchers and economists believed that humans made logical, well-considered decisions. In recent decades, however, researchers have uncovered a wide range of mental errors that derail our thinking. 5 Common Mental Errors That Sway You From Making Good Decisions: Let's talk about the mental errors that show up most frequently in our lives and break them down in easy-to-understand language. This blog outlines how survivorship bias, loss aversion, the availability heuristic, anchoring, and confirmation bias sway you from making good decisions. How to Spot a Common Mental Error That Leads to Misguided Thinking: Hundreds of psychology studies have proven that we tend to overestimate the importance of events we can easily recall and underestimate the importance of events we have trouble recalling. Psychologists refer to this little brain mistake as an “illusory correlation.” In this article, we talk about a simple strategy you can use to spot your hidden assumptions and prevent yourself from making an illusory correlation. Two Harvard Professors Reveal One Reason Our Brains Love to Procrastinate: We have a tendency to care too much about our present selves and not enough about our future selves. If you want to beat procrastination and make better long-term choices, then you have to find a way to make your present self act in the best interest of your future self. This article breaks down three simple ways to do just that. How to Use Mental Models for Smart Decision Making The smartest way to improve your decision making skills is to learn mental models. A mental model is a framework or theory that helps to explain why the world works the way it does. Each mental model is a concept that helps us make sense of the world and offers a way of looking at the problems of life.")
      post6=Post(title='Be more productive everyday', body="Let's define productivity. Productivity is a measure of efficiency of a person completing a task. We often assume that productivity means getting more things done each day. Wrong. Productivity is getting important things done consistently. And no matter what you are working on, there are only a few things that are truly important. Being productive is about maintaining a steady, average speed on a few things, not maximum speed on everything. Before we talk about how to get started, I wanted to let you know I researched and compiled science-backed ways to stick to good habits and stop procrastinating.  My Top Productivity Strategies One: Eliminate Time Wasting Activities by Using the Eisenhower Box: This simple decision matrix will help you take action, organize tasks, and get more done. The great thing about this matrix is that it can be used for broad productivity plans (“How should I spend my time each week?”) and for smaller, daily plans (“What should I do today?”). Two: Warren Buffett’s “2 List” Strategy: How to Maximize Your Focus and Master Your Priorities: This method comes from the famous investor Warren Buffett and uses a simple 3-step productivity strategy to help you determine your priorities and actions. You may find this method useful for making decisions and getting yourself to commit to doing one thing right away. Three: The Ivy Lee Method: The Daily Routine Experts Recommend for Peak Productivity: This productivity strategy is straightforward: Do the most important thing first each day. The Ivy Lee Method is a dead simple way to implement this strategy. Four: The 15-Minute Routine Anthony Trollope Used to Write 40+ Books: There is one common problem with the approach of ranking your priorities and doing the most important thing first, though. After ranking your priorities for the day, if the number one task is a really big project then it can leave you feeling frustrated because it takes a long time to finish. Writer Anthony Trollope, however, developed a solution to this common problem. Most productivity strategies focus on short-term efficiency: how to manage your to-do list effectively, how to get more done each morning, how to shorten your weekly meetings, and so on. These are all reasonable ideas. We often fail to realize, however, that there are certain strategic choices we need to make if we want to maximize our productivity for the long-term. In these articles below, I break down some ideas about long-term productivity. Here Are More Simple Ways to Be More Productive Every Day: Step 1: Manage your energy, not your time. If you take a moment to think about it, you’ll probably realize that you are better at doing certain tasks at certain times. What type of energy do you have in the morning? Afternoon? Evening? Determine what tasks each energy level and time of day are best suited for. Step 2: Prepare the night before. If you only do one thing each day then spend a few minutes each night organizing your to–do list for tomorrow. When I do it right, I’ll outline the article I’m going to write the next day and develop a short list of the most important items for me to accomplish. It takes 10 minutes that night and saves 3 hours the next day. Step 3: Don’t open email until noon. Sounds simple. Nobody does it. It took me awhile to get over the urge to open my inbox, but eventually I realized that everything can wait a few hours. Nobody is going to email you about a true emergency (a death in the family, etc.), so leave your email alone for the first few hours of each day. Use the morning to do what’s important rather than responding to what is “urgent.” Step 4: Turn your phone off and leave it in another room. Or on your colleague's desk. Or at the very least, put it somewhere that is out of sight. This eliminates the urge to check text messages, Facebook, Twitter, and so on. This simple strategy eliminates the likelihood of slipping into half–work where you waste time dividing your attention among meaningless tasks. Step 5: Work in a cool place. Have you ever noticed how you feel groggy and sluggish in a hot room? Turning the temperature down or moving to a cooler place is an easy way to focus your mind and body. (Hat tip to Michael Hyatt for this one.) Step 6: Sit up or stand up. When you sit hunched over, your chest is in a collapsed position and your diaphragm is pressing against the bottom of your lungs, which hinders your ability to breathe easily and deeply. Sit up straight or stand up and you’ll find that you can breathe easier and more fully. As a result, your brain will get more oxygen and you’ll be able to concentrate better. Step 7: Develop a “pre–game routine” to start your day. My morning routine starts by pouring a cold glass of water. Some people kick off their day with ten minutes of meditation. Similarly, you should have a sequence that starts your morning ritual. This tiny routine signals to your brain that it’s time to get into work mode or exercise mode or whatever mode you need to be in to accomplish your task. Additionally, a pre–game routine helps you overcome a lack of motivation and get things done even when you don’t feel like it.")
      post7=Post(title='Continous Improvement', body="Let's define continuous improvement. Continuous improvement is a dedication to making small changes and improvements every day, with the expectation that those small improvements will add up to something significant. The typical approach to self-improvement is to set a large goal, then try to take big leaps in order to accomplish the goal in as little time as possible. While this may sound good in theory, it often ends in burnout, frustration, and failure. Instead, we should focus on continuous improvement by slowly and slightly adjusting our normal everyday habits and behaviors. It is so easy to dismiss the value of making slightly better decisions on a daily basis. Sticking with the fundamentals is not impressive. Falling in love with boredom is not sexy. Getting one percent better isn't going to make headlines. There is one thing about it though: it works. How Does Continuous Improvement Work? So often we convince ourselves that change is only meaningful if there is some large, visible outcome associated with it. Whether it is losing weight, building a business, traveling the world or any other goal, we often put pressure on ourselves to make some earth-shattering improvement that everyone will talk about. Meanwhile, improving by just 1 percent isn't notable (and sometimes it isn't even noticeable). But it can be just as meaningful, especially in the long run. In the beginning, there is basically no difference between making a choice that is 1 percent better or 1 percent worse. (In other words, it won't impact you very much today.) But as time goes on, these small improvements or declines compound and you suddenly find a very big gap between people who make slightly better decisions on a daily basis and those who don't. Here's the punchline: If you get one percent better each day for one year, you'll end up thirty-seven times better by the time you’re done. This is why small choices don't make much of a difference at the time, but add up over the long-term.")
      post8=Post(title='We\'re talking about practise', body="Deliberate practice refers to a special type of practice that is purposeful and systematic. While regular practice might include mindless repetitions, deliberate practice requires focused attention and is conducted with the specific goal of improving performance.Can You Achieve Anything With Enough Practice?Deliberate practice does not mean that you can fashion yourself into anything with enough work and effort, though. While human beings do possess a remarkable ability to develop their skills, there are limits to how far any individual can go. Your genes set a boundary around what is possible. However, while genetics influence performance, they do not determine performance. Do not confuse destiny with opportunity. Genes provide opportunity. They do not determine our destiny. It’s similar to a game of cards. You have a better opportunity if you are dealt a better hand, but you also need to play the hand well to win. Regardless of where we choose to apply ourselves, deliberate practice can help us maximize our potential—no matter what cards we were dealt. It turns potential into reality. Read The Myth and Magic of Deliberate Practice for more on genetics, practice, and how to maximize your genetic potential in life. Examples of Deliberate Practice: Joe DiMaggio was one of the greatest hitters in baseball history. I recently heard a little-known story about how DiMaggio developed his exceptional ability. In some circles, golfer Ben Hogan is credited with “inventing practice.” Hogan methodically broke the game of golf down into chunks and figured out how he could master each section. Today, experts have a new term for his rigorous style of improvement.")
      db.session.add(post1)
      db.session.add(post2)
      db.session.add(post3)
      db.session.add(post4)
      db.session.add(post5)
      db.session.add(post6)
      db.session.add(post7)
      db.session.add(post8)
      db.session.commit()