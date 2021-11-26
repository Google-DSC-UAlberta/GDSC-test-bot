require('dotenv').config(); //initialize dotenv
const Discord = require('discord.js');
const { Client, Intents } = require('discord.js');

const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

var timer; 
client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

client.on('messageCreate', msg => {
  switch (msg.content) {
    case "test":
      msg.reply('GDSC!');
      break;
    case "time":
      msg.reply('Timer have been started!');
      timer = setInterval(() => msg.channel.send(`The Current Time is: ${new Date().toString()}`), 5000);
      break;
    case "clear":
      if (timer) {
        clearInterval(timer);  
        msg.reply('Timer have been cleared!');
      } else {
        msg.reply('A timer is not started yet! Type "time" to start the timer.');
      }
      timer = null;
    case "code":
      msg.reply(
        "\`\`\`js" + "\n" +
        "console.log('just showing a little javascript snippet!');" + "\n" +
        "\`\`\`"
      );
  }

});

//make sure this line is the last line
client.login('OTEzODIzNjQyNDc4MDU1NDM2.YaEGlg.p-D7ebFGw9CQ5CD0GTOirZ_Molo'); //login bot using token