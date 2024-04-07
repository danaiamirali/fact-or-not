from foxornot.utils import text

string = """The United States Capitol

Good evening. 

Mr. Speaker. Madam Vice President. Members of Congress. My Fellow Americans. 

In January 1941, President Franklin Roosevelt came to this chamber to speak to the nation. 

He said, “I address you at a moment unprecedented in the history of the Union.” 

Hitler was on the march. War was raging in Europe. 

President Roosevelt’s purpose was to wake up the Congress and alert the American people that this was no ordinary moment.   

Freedom and democracy were under assault in the world. 

Tonight I come to the same chamber to address the nation. 

Now it is we who face an unprecedented moment in the history of the Union. 

And yes, my purpose tonight is to both wake up this Congress, and alert the American people that this is no ordinary moment either. 

Not since President Lincoln and the Civil War have freedom and democracy been under assault here at home as they are today. 

What makes our moment rare is that freedom and democracy are under attack, both at home and overseas, at the very same time. 

Overseas, Putin of Russia is on the march, invading Ukraine and sowing chaos throughout Europe and beyond. 

If anybody in this room thinks Putin will stop at Ukraine, I assure you, he will not. 

But Ukraine can stop Putin if we stand with Ukraine and provide the weapons it needs to defend itself. That is all Ukraine is asking. They are not asking for American soldiers. 

In fact, there are no American soldiers at war in Ukraine. And I am determined to keep it that way. 

But now assistance for Ukraine is being blocked by those who want us to walk away from our leadership in the world. 

It wasn’t that long ago when a Republican President, Ronald Reagan, thundered, “Mr. Gorbachev, tear down this wall.” 

Now, my predecessor, a former Republican President, tells Putin, “Do whatever the hell you want.” 

A former American President actually said that, bowing down to a Russian leader. 

It’s outrageous. It’s dangerous. It’s unacceptable. 

America is a founding member of NATO the military alliance of democratic nations created after World War II to prevent war and keep the peace.  

Today, we’ve made NATO stronger than ever. 

We welcomed Finland to the Alliance last year, and just this morning, Sweden officially joined NATO, and their Prime Minister is here tonight. 

Mr. Prime Minister, welcome to NATO, the strongest military alliance the world has ever known. 

I say this to Congress: we must stand up to Putin. Send me the Bipartisan National Security Bill. 

History is watching. 

If the United States walks away now, it will put Ukraine at risk. 

Europe at risk. The free world at risk, emboldening others who wish to do us harm. 
 
 

My message to President Putin is simple.  

We will not walk away. We will not bow down. I will not bow down. 

History is watching, just like history watched three years ago on January 6th. 

Insurrectionists stormed this very Capitol and placed a dagger at the throat of American democracy. 

Many of you were here on that darkest of days. 

We all saw with our own eyes these insurrectionists were not patriots. 
 

They had come to stop the peaceful transfer of power and to overturn the will of the people. 

January 6th and the lies about the 2020 election, and the plots to steal the election, posed the gravest threat to our democracy since the Civil War. 

But they failed. America stood strong and democracy prevailed. 

But we must be honest the threat remains and democracy must be defended. 

My predecessor and some of you here seek to bury the truth of January 6th. 

I will not do that. 

This is a moment to speak the truth and bury the lies. 

And here’s the simplest truth. You can’t love your country only when you win. 

As I’ve done ever since being elected to office, I ask you all, without regard to party, to join together and defend our democracy! 

Remember your oath of office to defend against all threats foreign and domestic. 

Respect free and fair elections! Restore trust in our institutions! And make clear –political violence  

has absolutely no place in America! 

History is watching. 

And history is watching another assault on freedom.  

Joining us tonight is Latorya Beasley, a social worker from Birmingham, Alabama. 14 months ago tonight, she and her husband welcomed a baby girl thanks to the miracle of IVF. 

She scheduled treatments to have a second child, but the Alabama Supreme Court shut down IVF treatments across the state, unleashed by the Supreme Court decision overturning Roe v. Wade. 

She was told her dream would have to wait. 

What her family has gone through should never have happened. And unless Congress acts, it could happen again. 

So tonight, let’s stand up for families like hers! 

To my friends across the aisle, don’t keep families waiting any longer. Guarantee the right to IVF nationwide! 

Like most Americans, I believe Roe v. Wade got it right. And I thank Vice President Harris for being an incredible leader, defending reproductive freedom and so much more. 

But my predecessor came to office determined  

to see Roe v. Wade overturned. 

He’s the reason it was overturned. In fact, he brags about it. 

Look at the chaos that has resulted. 

Joining us tonight is Kate Cox, a wife and mother  

from Dallas. 

When she became pregnant again, the fetus had a fatal condition. 

Her doctors told Kate that her own life and her ability to have children in the future were at risk if she didn’t act. 

Because Texas law banned abortion, Kate and her husband had to leave the state to get the care she needed. 

What her family has gone through should never have happened as well. But it is happening to so many others. 

There are state laws banning the right to choose, criminalizing doctors, and forcing survivors of rape and incest to leave their states as well to get the care they need. 

Many of you in this Chamber and my predecessor are promising to pass a national ban on reproductive freedom. 

My God, what freedoms will you take away next? 

In its decision to overturn Roe v. Wade the Supreme Court majority wrote, “Women are not without – 

electoral or political power.” 

No kidding. 

Clearly, those bragging about overturning Roe v. Wade have no clue about the power of women in America."""

from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
)

txt = text.split_into_statements(llm, string)
print(txt)

txt = text.check_from_text(llm, string)
print(txt)