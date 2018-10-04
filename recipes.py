import requests, bs4, sys, pyperclip

def getIngredients(recipes):
    # Variable Declaration
    finalText = ''

    for recipe in recipes: # Loop through all recipes given
        # Grab site HTML / check if valid
        site = requests.get(recipe)
        if site.status_code == requests.codes.ok:
            siteCode = bs4.BeautifulSoup(site.text, 'html.parser')
            servings = siteCode.find('span', attrs={'class': 'wprm-recipe-details wprm-recipe-servings'}).text

            recipeList = [] # Holds recipe data

            # Adds title and URL
            title = siteCode.find('h1', attrs={'class': 'title'})
            recipeList.append(title.text)
            recipeList.append(recipe)

            # Loops through ingredients, adds them, and joins everything into a string
            ingredients = siteCode.find_all('li', attrs={'class': 'wprm-recipe-ingredient'})
            for i in range(len(ingredients)):
                changeServings = ingredients[i].text.replace('\n', ' ')
                changeServings = changeServings.split(' ')
                if changeServings[1].isnumeric():
                    changeServings[1] = str(round((float(eval(changeServings[1])) / int(servings)) * 6, 2))
                changeServings = ' '.join(changeServings)
                recipeList.append(changeServings)

            finalText += '\n'.join(recipeList)
            finalText += '\n\n'

        else:
            print('URL ERROR')

    return finalText

if len(sys.argv) > 1:
    pyperclip.copy(getIngredients(sys.argv[1:]))

else:
    print('Must have at least one URL')