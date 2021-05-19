about_page = '''
## Our Mission
Imperium is a data visualisation app that serves investigative journalists and concerned citizens with the knowledge they require and deserve. 
For too long we have had no idea what goes on in Brussels. Imperium aims to change that.
Our mission is provide the most up-to-date information and combine this with intuitive data visualisations. 
Like this, everyone has the ability to learn more about what goes on at the heart of Europe. 
We hope that our platform can be of use to you and possibly result in positive changes due to increased awareness.

##### Our Data
We provide data that comes directly from the EU Transparency Register with some additional preprocessing steps by [LobbyFacts](https://lobbyfacts.eu/).
Each organisation in this register provides the following data:
- The organisation name
- The location of their head office
- The category this organisation belongs to (eg. law firms, educational organisation, etc)
- Their estimated lobbying costs
- The amount of EP passes
- Amount of lobbyists under their employ
- Date of registration

We let users filter on subsets of this data in order to observe interesting visualisations.

##### Get Started
In case you don't know where to start exploring, we have a couple of tips for you to kickstart your journey!

- Take a look at our world map. Do you see that Belgium has an incredible amount of registered organisations, even when compared to much bigger countries within the EU. Why could that possibly be?
    - Hint: Remind me again, where is the European Parliament located?
- Select Facebook in our organisation filter. Do you see that steady rise since 2016 that really accelerates in 2018. Why on earth would that be?
    - Hint: This might be pure coincidence (wink wink) but GDPR was adopted in 2016 and really went into effect in 2018...


##### Terminology
We realise that not everyone understands the jargon that is used in official EU documents. 
As such we provide a quick overview of several terms that are often used.

| Term | Explanation | Additional info |
|:-:|:-:|:-:|
| EP Passes | EP Passes stands for European Parliament passes.  Simply put, it means how many access passes this organisation has to the European parliament. |  |
| Lobbyists (FTE) | This terms means lobbyists or Full Time Equivalents. | We have included employees spending 5% or more of their time engaged in relevant activities under the 25% band. |
| # of meetings | This simply means the total number of meetings with parliamentarians that occurred. |  |
| Average spending | As the dataset only provides a range of spending, we are sometimes forced to calculate an estimate of the spending. To do this, we take the average between the minimum and maximum of the range. | As an example, say a company reports a range of 0 to 100 euros. The average spending would be 50 euros. |

##### Known Issues

There are several known issues both with the dataset. We present an overview below with an explanation regarding these problems.

1. The spending is only an approximation
    - You are completely right in noticing this.
    There is however nothing that we can do here, as the EU allows companies to give a range of spending rather than a concrete number. 
    We don't like it either, so maybe if we all raise our voices they'll change it one day!
2. Some of the organisations in the dataset show extreme spikes in spending, what is that about?
    - The authorities in charge of the transparency register appear to be extremely lenient towards organisations and does not actively check submissions. 
    We, as well as other people, have noticed several of these anomalies and suspect this is due to input errors of the organisations themselves.
    As there is no way of knowing which data inputs are errors and which are actually correct, we leave the data as is.
3. The organisations tab can load slowly when comparing
    - This is a problem with the hosting provider we use for our platform. As we are only students, we have opted for a free plan which offers only limited speeds.

#### Created by Willem Ropke, Sofyan Ajridi and Thomas Vaeyens



'''