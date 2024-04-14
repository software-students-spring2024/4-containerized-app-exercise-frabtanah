#add correct imports 


class TestMood: 

    def test_coffee_suggestion(self):

        suggestion = coffee_suggestion()

        assert suggestion.startswith("How about a cup of ")
        prefix = "How about a cup of "
        suffix = " today?"
        coffee_type = suggestion[len(prefix):-len(suffix)]
        assert coffee_type in coffee_types, f"Extracted coffee type was '{coffee_type}'"


    def test_return_tip_from_specified_category(self):
        """
            Test if the function returns a tip from the specified category.
        """
        for category in relaxation_tips.keys():
            tip = relaxation_tip(category)
            assert tip in relaxation_tips[category], f"The tip should be from the {category} category."

    def test_return_tip_with_no_category(self):
        """
            Test if the function returns a tip when no category is specified.
        """
        tip = relaxation_tip()
        all_tips = [item for sublist in relaxation_tips.values() for item in sublist]
        assert tip in all_tips, "The function should return a valid tip when no category is specified."
    

    def test_relaxation_tip_variety(self):
        """
            Test if the function returns a variety of unique tips when called multiple times.
        """
        tips = [relaxation_tip() for _ in range(10)]  #call the function multiple times
        unique_tips = set(tips)  #convert the list of tips to a set to remove duplicates
        assert len(unique_tips) > 1, "The function should return a variety of tips."


    def test_cat_mood_generator(self):
        expected_moods = ["Playful", "Sleepy", "Hungry", "Grumpy"]
        
        mood = cat_mood_generator()
        
        assert mood in expected_moods, f"The mood {mood} is not in the list of expected moods."


    ## Testing high_five expected output
    def test_high_five_expected(self):

        expected_output = highfives
        hf = high_five()
        assert hf in expected_output, f"The high five {hf} is not as expected."
    
    ## Testing if high_five is a string 
    def test_high_five_string(self):

        hf = high_five()
        assert isinstance(hf, str)


    ## Testing if high_five is random variety
    def test_high_five_variety(self):

        hfs = [high_five() for _ in range(15)]  #call the function 15 times
        unique_hfs = set(hfs)  
        assert len(unique_hfs) > 1, "The function should return a variety of hfs."


    
    # Testing if a string is returned
    def test_joke_string(self):
        joke = tell_me_a_joke()
        assert isinstance(joke, str)
    
    # Testing if the joke is a valid joke from the list.
    def test_joke_valid(self):
        joke = tell_me_a_joke()
        assert joke in jokes, f"The joke {joke} is not in the list of expected moods."
    
    # Testing if the joke is random each time.
    def test_joke_random(self):
        joke = [tell_me_a_joke() for _ in range(10)]  #call the function multiple times
        joke_set = set(joke)  #convert the list of tips to a set to remove duplicates
        assert len(joke_set) > 1, "The function should return a random joke each time."
        