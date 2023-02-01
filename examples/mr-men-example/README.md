# Mr Men Examples
 You have been given a set of data on various 'Mr Men' and 'Little Miss' characters. You need to combine the required data into a single file

 ## Example 1
 This example requires a `parameter`. The key is `Adjective` and the value is an the adjective you'd like to be the character's surname.

 The output file will return the character(s) found under the `CharactersFound` key.

 ## Example 2
 This example requires you to seperate male and females between `Male` and `Femaile` keys (using their naming convention of "mr" vs "little miss"). You must then list the skin colours of all male and female colours under the key `SkinColour`.
 This is a good example of [dfm's merging logic](https://github.com/ServerlessSam/data-file-merge/wiki/Merging-Logic). Our first merge is a `string` into another `string`, producing a list of `["string1", "string2"]`. Each subsiquent merge is a `string` into a `list` which will append the list with that string.