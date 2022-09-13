<!-- BOT -->
## BOT
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Bot">Bot</a>
      <ul>
        <li><a href="#commands">Commands</a></li>
      </ul>
      <ul>
        <li><a href="#callbacks">Callbacks</a></li>
      </ul>
      <ul>
        <li><a href="#voice">Voice recognition functions</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- COMMANDS -->
## Commands

<br>Start command return message with your text if chat type is "private".</br>
<br>Mute command return text message with keyboard if chat type is "supergroup" and the message is a reply to a message bot get chat member status and mute member if counter = 10.</br>
<br>Unmute command return message if member who call command is "administrator" and message is reply to message, removes all restrictions except sending stickers.</br>
<br>Faq command return keyboard with text if chat type is "private", keyboard generates by using web service.</br>
<br>Recognize command return text if message is a reply to message and is a voice message, call recognize_voice function and reply to command message.</br>
<br>New chat members handler react to join to group new members, send data to web service.</br>

<!-- CALLBACKS -->
## CALLBACKS
<br>Callback is a reaction to push keyboard button and other inline activity.</br>
<br>Faq callbacks react to push button in faq keyboard and call function [get_faq](https://github.com/Cybeear/tg-chat-project/blob/7f7790788a71157f28603b21be0f64c667931200/bot/handlers/functions.py#L19), return text message.</br>
<br>Mute callback react to push button in mute keyboard and call function ################</br>
<br>Welcome callback is a callback captcha, if member join group boy mute member and send message with keyboard reply to user, if user press the button bot unmute member.</br>


<!-- VOICE -->
## Voice

<br>recognize_voice receive voice file object and language string parameters,call transcibe_voice function to transcribe and download file, use Speech Recognition package recognize voice and return text, useng google service, and delete voice file after recognize.</br>
<br>transcibe_voice receive voice file object and path to save parameters, call download_voice function and transcribe voice file to wav format, use ffmpeg.</br>
<br>download_voice receive type of file, path and filename, async download file.</br>

<!-- FUNCTIONS -->
## FUNCTIONS

<br>get_warn receive user_id parameter, send get request to web service, return json object.</br>
<br>mute_time receive user_id parameter, get_warn function, calculate restriction time.</br>
<br>get_faq send get request to web service, return dict.</br>
<br>push_user receive user parameter, send post request to web service, return bool.</br>

