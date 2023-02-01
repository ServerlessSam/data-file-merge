# Shopping List Examples
 Jack and Jill are going shopping, the grandparents have asked if they can do their shopping too whilst they are there. To keep thing's simple, Jack/Jill want to combine everyone's lists into a single list, luckily everyone provided their list in JSON format!

 ## Example 1
 The dfm config file uses the `**` and `*` syntax from pathlib to ensure grandma and grandpa's shopping lists are included, even though they are in a nested directory. In fact, anyone's lists will be included that are within the example's directory. Try adding another file (or nest it within a directory too if you'd like) containing your own shopping list if you'd like Jack and Jill to pick something up for you.
 
 Your output file should be of the same format as everyone's lists, except combining the contents of everyone's lists.

 ## Example 2
 A slightly more complex version of Example 1. This time Jack and Jill want to seperate their grandparent's list from their own. They decide to use a seperate key (`ToBuyForGrandparents`) to contain the combined shopping list for them. Jack and Jill's lists are combined as per example 1.
 See if you can add another `SourceFile` to the dfm config to write your own shopping list to the output file under the key `ToBuyForMe`.