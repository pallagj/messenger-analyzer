# messenger-analyzer
`Facebook Messenger` message analyzer program. With the program, you can see who you talked to the most, see graphs of the amount of conversation, and more. 😎

This program is designed to analyze and generate statistics from messenger data. Here's a brief summary of the statistics it calculates:

2. **Messages Count:**
   - It calculates the total number of messages for each chat.

4. **Participant Count:**
   - It counts the number of messages sent by each participant in a given chat.

5. **Messages by Time:**
   - It groups messages by time (daily interval) and returns the count of messages for each time interval.
   
   ![image](https://github.com/pallagj/messenger-analyzer/assets/37118052/e5eea9c9-d96b-49b8-93e8-f42c6ada5e05)

6. **Messages by Time by Sender:**
   - Similar to the previous one, but it also distinguishes messages by sender.

8. **Reaction Matrix:**
   - It generates a matrix showing how often participants reacted to each other's messages.

![image](https://github.com/pallagj/messenger-analyzer/assets/37118052/e0db7511-b039-473e-92f6-1ae9a6fca2c6)




9. **Reaction Counts by Participant:**
   - It provides the count of each reaction for each participant, sorted by frequency.

Please note that the program uses the pandas library for data manipulation and assumes the existence of a `get_messenger_json` function in a module named `loader`.
