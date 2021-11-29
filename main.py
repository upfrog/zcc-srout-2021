import requests

def get_data_and_loop():

    url = 'https://zcccentredaxue.zendesk.com/api/v2/tickets.json?page[size]=25'
    user = 'upfrog43@gmail.com' + '/token'
    token = 'ldcF1f9L8jCekJfpai3yJSEuBEuB22VgjuowLLkj'
    # use this to count how many times you page forward. Subtract as you page back.
    times_can_page_back = 0

    while url:
        data = requests.get(url, auth=(user, token))
        if data.status_code != 200:
            print('An unexpected error has occurred. Error code: ', data.status_code,
                  '\nExiting.')
            exit()

        data = data.json()

        # This is the core of the loop: The current set of tickets are printed, then
        # the menu is displayed and the user can provide input
        print_all_tickets(data)
        print("\n")
        next_or_prev = menu_loop(data)

        # This responds to user input. There are three cases:
        #   paging forward when possible
        #   paging backward when possible
        #   killing the request URL, breaking the while loop.

        if next_or_prev == 0:
            if data['meta']['has_more']:
                url = data['links']['next']
                times_can_page_back = times_can_page_back + 1
            else:
                print("There are no more tickets to view.")
        elif next_or_prev == 1:
            if times_can_page_back > 0:
                url = data['links']['prev']
                times_can_page_back = times_can_page_back - 1
            else:
                print("There are no more tickets to return to.")
        else:
            url = None


'''
    handles input to bring a specific ticket into focus with more details. The string is
    built and printed in the helper function print_high_detail().
'''
def focus_ticket(data):
    ticket_ID = input("what is the ID of the ticket you want to access?")
    ticket_ID = int(ticket_ID) - 1  # compensates for off by 1 and casts so input can be used as index.
    data = data['tickets']

    print_high_detail(data, ticket_ID)

''' 
    Assembles and prints the string for the detailed ticket view. Construction is relatively
    verbose to enhance clarity. 
'''
def print_high_detail(data, ticket_ID):
    id = str(data[ticket_ID]['id'])
    subject = data[ticket_ID]['subject']  # MAY CUT THIS OUT
    priority = str(data[ticket_ID]['priority'])
    requester = str(data[ticket_ID]['requester_id'])
    submitter = str(data[ticket_ID]['submitter_id'])
    assignee = str(data[ticket_ID]['assignee_id'])
    time_created = data[ticket_ID]['created_at']
    time_updated = data[ticket_ID]['updated_at']
    description = data[ticket_ID]['description']
    status = data[ticket_ID]['status']

    print("\nTicket ID: " + id + "\nRequester ID: " + requester + "\nSubmitter ID: " + submitter \
          + "\nAssignee ID: " + assignee + "\nCurrent status: " + status \
          + "\nCreated: " + time_created + "\nLast updated: " + time_updated + "\nPriority: " + priority \
          + "\n" + "\nDescription: \n" + description + "\n")

'''
    prints all tickets with relatively little detail. This function handles the control
    loop, and spacing, but not the assembly and printing of the string itself, which is 
    left to print_low_detail().
'''
def print_all_tickets(data):
    data = data['tickets']
    count = 0
    for tickets in data:
        # occasionally inserts a line break for readability
        if count % 5 == 0:
            print("\n")
        else:
            print("")

        count = count + 1
        print_low_detail(tickets)

'''
    Assemples and prints a relatively un-detailed ticket view.
'''
def print_low_detail(data):
    id = str(data['id'])
    subject = data['subject']
    priority = str(data['priority'])
    requester = str(data['requester_id'])
    time_created = data['created_at']
    status = data['status']

    output = "Ticket " + id + ": " + subject + ". Priority: " \
             + priority + ". Requester: " + requester \
             + ". Created: " + time_created + ". Status: " + status

    print(output, end = '')




'''
    This is the core user interaction loop. It can only be exited by changing the 
    tickets on display (paging back or forward, focussing), or quitting the program.
    
    The structure of the conditionals is as follows:
        is the input an integer?
            If yes, is it a 1, a 2, or something else?
                If it is 1 or 2, the view is refreshed or the ticket-focus process starts.
                if it is something else, an error message is shown and new input is prompted.
            If no, then is it an "n", a "p", or something else?
                If it is "n" or "p", then tickets are paged forward or backward.
                If it is something else, an error message is shown and new input is prompted.
'''
def menu_loop(data):
    loop = True

    while loop:  ## While loop which will keep going until loop = False
        print("press 1 to view all tickets.")
        print("press 2 to view one ticket.")
        print("press \"n\" to proceed to the next page")
        print("press \"p\" to return to the previous page")
        print("type \"quit\" to exit")
        choice = input("input: ")

        # Try-catch statement checks if input is an integer by checking for
        # failure of int-casting.
        try:
            choice = int(choice)

            if choice == 1:  # Print all tickets
                print_all_tickets(data)
            elif choice == 2:  # Focus on a specific ticket
                focus_ticket(data)
            else:  # Invalid integer input is rejected
                print("Invalid input: input is not a valid choice. Please try again")

        except ValueError:
            if choice.lower() == ("quit"):
                print("Thanks for using the viewer! Have a wonderful day!")
                exit()

            # These two elifs tell the data fetching method to page forward or backwards.
            elif choice.lower() == ("n"):
                return 0  # Having this function return things may not work, as a return may not be guaranteed.
            elif choice.lower() == ("p"):
                return 1
            # Covers invalid string inputs.
            else:
                print("Invalid input: input is not an integer. Please try again.")


def main():
    get_data_and_loop()


if __name__ == '__main__':
    main()
