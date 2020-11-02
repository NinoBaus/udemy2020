num_years = input('Please input the number of years: ')

def years(num_years):
    try:
        num_years = int(num_years)
        if num_years > 50:
            print("You are old")
        else:
            print("You are young")
    except ValueError:
         print('You cannot use a character other than a number for this input')
         retry = input('Try again? ')
         if retry == 'yes' or 'y' or 'Yes' or 'Y':
            pass

years(num_years)