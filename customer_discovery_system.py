# Customer Discovery Intelligence System
# This system is designed to help businesses prioritize their prospects based on the Ideal Customer Profile (ICP) classification. 
# It will read the interview data from a text file, calculate the ICP score for each prospect, classify them into tiers, 
# and provide insights and recommendations for engagement.
def main():
    print("\nWelcome to Customer Discovery Intelligence System")
    start_menu()

#This function will generate a summary of the ranked prospects based on their Ideal Customer Profile (ICP) classification.
def generate_prospect_summary():
    ranked_prospects = get_ranked_prospects()
    total_prospects = len(ranked_prospects)
    high_priority = 0
    medium_priority = 0
    low_priority = 0
    for prospect in ranked_prospects:
        if prospect["classification"] == "Tier 1 ICP":
            high_priority += 1
        elif prospect["classification"] == "Tier 2 ICP":
            medium_priority += 1
        else:
            low_priority += 1
    summary = {
        "total_prospects": total_prospects,
        "high_priority": high_priority,
        "medium_priority": medium_priority,
        "low_priority": low_priority,
        "top_prospect": ranked_prospects[0]["organization_name"]
    }
    return summary


#This function will provide the reasons for prioritizing a prospect based on their interview data.
#  It will check the importance score, cost concern, technology interest, and pilot readiness of the prospect and return a list of reasons why that prospect is prioritized.
def get_priority_reason(interview_data):
    reasons = []
    if interview_data["importance_score"] >= 8:
        reasons.append("High importance score")
    if interview_data["cost_concern"] >= 8:
        reasons.append("High cost concern")
    if interview_data["tech_interest"] >= 8:
        reasons.append("Strong technology interest")
    if interview_data["pilot_readiness"] == "Yes":
        reasons.append("Pilot ready")
    return reasons


#This function will provide a recommendation for the next steps to engage with a prospect based on their Ideal Customer Profile (ICP) classification. 
# The function takes the ICP classification as input and returns a recommendation for how to proceed with that prospect.
def get_prospect_recommendation(classification):
    if classification == "Tier 1 ICP":
        return "Immediate Pilot Discussion"
    elif classification == "Tier 2 ICP":
        return "Continue Engagement"
    else:
        return "Low Priority Prospect"

# This function will display the ranked list of prospects based on their Ideal Customer Profile (ICP) score and classification. 
# It will call the "get_ranked_prospects" function to get the ranked list of prospects
def display_prospect_rankings():
    ranked_prospects = get_ranked_prospects()
    #print("\nProspect Prioritization Report")
    print("\nRanked Prospects are as follows:")
    print("----------------------------------")
    rank = 1
    for prospect in ranked_prospects:
        recommendation = get_prospect_recommendation(prospect["classification"])
        reasons = get_priority_reason(prospect)
        print(f"\n{rank}. {prospect['organization_name']}")
        print(f"ICP Score: {prospect['score']} / {prospect['max_score']}")
        print(f"Classification: {prospect['classification']}")
        print(f"Recommendation: {recommendation}")
        if prospect["classification"] == "Not ICP":
            print("\nWhy Not Prioritized?")
            print("- Poor score on key ICP factors such as importance, cost concern, tech interest, and pilot readiness")
        else:
            print("\nWhy Prioritized?")
        for reason in reasons:
                print(f"- {reason}")
        
        rank += 1

#This function will read the "interviews.txt" file, extract the relevant data for each interview, calculate the Ideal Customer Profile (ICP) score for each customer
#  using the "calculate_icp_score" function, classify each customer as Tier 1 ICP, Tier 2 ICP, or Not ICP using the "classify_icp" function, 
# and return a list of dictionaries containing the ICP score, maximum possible score, and classification for each customer. 
# The function will then sort this list of dictionaries based on the ICP score in descending order and return the ranked list of prospects.
def get_ranked_prospects():
    icp_results = get_all_icp_results()
    ranked_prospects = sorted(
        icp_results,
        key=lambda prospect: prospect["score"],
        reverse=True
    )
    return ranked_prospects

#This function will display a summary of the Ideal Customer Profile (ICP) based on the interviews conducted. 
# It will call the "generate_icp_summary" function to get the summary data and then print it in a readable format for the user.
def display_icp_summary():
    summary = generate_icp_summary()
    print("\nIdeal Customer Profile (ICP) Summary:")
    print('---------------------------------')
    print(f"\nTotal Interviews: {summary['Total Interviews']}")
    print(f"\nTier 1 ICP: {summary['Tier 1 ICP']}")
    print(f"\nTier 2 ICP: {summary['Tier 2 ICP']}")
    print(f"\nNot ICP: {summary['Not ICP']}")
    print(f"\nHighest ICP Score: {summary['Highest ICP Score']} out of 70")
    print(f"\nAverage ICP Score: {summary['Average ICP Score']:.2f} out of 70")

def generate_icp_summary():
    #This function will generate a summary of the Ideal Customer Profile (ICP) based on the interviews conducted. 
    # The function will read the "interviews.txt" file, extract the relevant data for each interview, and 
    # calculate the ICP score for each customer using the "calculate_icp_score" function. 
    # The function will then classify each customer as Tier 1 ICP, Tier 2 ICP, or Not ICP using the "classify_icp" function, 
    # and return a summary of the ICP classifications for all customers.
    interviews = get_all_interviews()
    summary = {
        "Total Interviews": 0,
        "Tier 1 ICP": 0,
        "Tier 2 ICP": 0,
        "Not ICP": 0,
        "Highest ICP Score": 0,
        "Average ICP Score": 0
    }
    total_scores = 0
    for interview in interviews:
        if interview != "":
            interview_data = eval(interview)
            classification = classify_icp(interview_data)
            score = calculate_icp_score(interview_data)
            summary["Total Interviews"] += 1
            summary[classification] += 1
            total_scores += score
            if score > summary["Highest ICP Score"]:
                summary["Highest ICP Score"] = score
    if summary["Total Interviews"] > 0:
        summary["Average ICP Score"] = round(
    total_scores / summary["Total Interviews"],
    2
)
    return summary
     


#This function will read the "interviews.txt" file, extract the relevant data for each interview, 
# calculate the Ideal Customer Profile (ICP) score for each customer using the "calculate_icp_score" function, 
# classify each customer as Tier 1 ICP, Tier 2 ICP, or Not ICP using the "classify_icp" function, and 
# return a list of dictionaries containing the ICP score, maximum possible score, and classification for each customer.
def get_all_icp_results():
    interviews = get_all_interviews()
    results = []
    for interview in interviews:
        if interview != "":
            #interview_data = eval(interview)
            #print(repr(interview))
            interview_data = eval(interview)
            score = calculate_icp_score(interview_data)
            classification = classify_icp(interview_data)
            results.append(
                {   "organization_name": interview_data["organization_name"],
                    "score": score,
                    "max_score": 70, # Assuming the maximum possible ICP score is 70 based on the scoring system defined in calculate_icp_score function
                    "classification": classification,
                    "importance_score": interview_data["importance_score"],
                    "cost_concern": interview_data["cost_concern"],
                    "tech_interest": interview_data["tech_interest"],
                    "pilot_readiness": interview_data["pilot_readiness"],
                }
            )
    return results

# This function will classify a customer as Tier 1 ICP, Tier 2 ICP, or Not ICP based on their calculated ICP score and pilot readiness. 
# The function takes a customer dictionary as input, calculates the ICP score using the "calculate_icp_score" function,
# and returns the appropriate classification.
def classify_icp(customer):
    icp_score = calculate_icp_score(customer)
    pilot_ready = customer["pilot_readiness"]
    if icp_score >= 50 and pilot_ready == "Yes":
        return "Tier 1 ICP"
    elif icp_score >= 40:
        return "Tier 2 ICP"
    else:
        return "Not ICP"

# This function will read the "interviews.txt" file, extract the relevant data for each interview, and 
# calculate the Ideal Customer Profile (ICP) score for each customer based on their facility size and other relevant factors. 
# The function will return a list of ICP scores for all customers.
def get_all_icp_scores():
    interviews = get_all_interviews()
    icp_scores = []
    for interview in interviews:
        if interview != "":
            interview_data = eval(interview) #converting the string representation of the dictionary back to a dictionary
            icp_score = calculate_icp_score(interview_data)
            icp_scores.append(icp_score)
    return icp_scores


def calculate_icp_score(customer):
    #This function will calculate the Ideal Customer Profile (ICP) score for a given customer based on their facility size and other relevant factors. 
    #The function will take a customer dictionary as input, extract the facility size from the dictionary, and 
    # then call the "get_facility_size_points" function to get the corresponding points for that facility size. 
    # The function will then return the calculated ICP score for the customer.
    #facility_size = customer["facility_size"]
    #icp_score = get_facility_size_points(facility_size)
    #return icp_score
    importance = customer["importance_score"]

    tech_interest = customer["tech_interest"]

    cost_concern = customer["cost_concern"]

    facility_points = get_facility_size_points(customer["facility_size"])

    icp_score = (
        importance * 3
        + tech_interest
        + cost_concern * 2
        + facility_points * 2
        )

    return icp_score

#This function will take the facility size as input and return a corresponding point value based on the defined categories. 
# The function uses a series of if-elif statements to check the input facility size against the predefined categories and assigns points accordingly. 
# If the input does not match any of the predefined categories, it returns a default point value of 3 for unknown facility sizes.
def get_facility_size_points(facility_size):

    if facility_size == "<100":
        return 1
    elif facility_size == "100 to 500":
        return 2
    elif facility_size == "501 to 2000":
        return 3
    elif facility_size == "2001 to 10000":
        return 4
    elif facility_size == "10000+":
        return 5
    else:
        return 3 #default points for unknown facility size


#this function will read the "interviews.txt" file, extract the "facility_size" field from each interview, and 
# count how many customers fall into each facility size category. The function will return a dictionary 
# with the facility size categories as keys and the count of customers in each category as values.
def get_facility_size_distribution():
    interviews = get_all_interviews()
    size_distribution = {
        "<100": 0,
        "100 to 500": 0,
        "501 to 2000": 0,
        "2001 to 10000": 0,
        "10000+": 0,
        "Unknown": 0
    }
    for interview in interviews:
        if interview != "":
            interview_data = eval(interview) #converting the string representation of the dictionary back to a dictionary
            facility_size = interview_data["facility_size"]
            if facility_size in size_distribution:
                size_distribution[facility_size] += 1
            else:
                size_distribution["Unknown"] += 1
    return size_distribution

#this function will read the "interviews.txt" file, split the data by new lines, and return a list of interviews. Each interview will be stored as a string in the list. 
# The function will be used to get all the interviews data for further processing in other functions.
def get_all_interviews():
    data = load_data("interviews.txt")
    interviews = data.split("\n")
    return interviews

# This function will calculate the percentage of customers who are ready for a pilot program by calling the "calculate_pilot_ready_count" 
# function to get the count of customers who are ready for a pilot program and the "count_interviews" function to get the total number of interviews conducted. 
# The function will then calculate the percentage by dividing the count of customers who are ready for a pilot program by the total number of interviews and multiplying by 100. 
# If there are no interviews conducted, the function will return 0 to avoid division by zero error.
def pilot_readiness_percentage():
    total_interviews = count_interviews("interviews.txt")
    pilot_ready_count = calculate_pilot_ready_count()
    if total_interviews > 0:
        return (pilot_ready_count / total_interviews) * 100
    else:
        return 0

# This function will calculate the number of customers who are ready for a pilot program by reading the "interviews.txt" file,
#  extracting the "pilot_readiness" field from each interview, and counting how many of them have a value of "Yes". The function will return the count of customers who are ready for a pilot program.
def calculate_pilot_ready_count():
    interviews = get_all_interviews()
    pilot_ready_count = 0
    for interview in interviews:
        if interview != "":
            interview_data = eval(interview) #converting the string representation of the dictionary back to a dictionary
            if interview_data["pilot_readiness"] == "Yes":
                pilot_ready_count += 1
    return pilot_ready_count

#This will calculate the average score for a given metric by reading the "interviews.txt" file, extracting the relevant scores for that metric, 
# and then calculating the average. The function takes the name of the metric as an argument and returns the average score for that metric across all interviews.
def calculate_average(metric_name):
    interviews = get_all_interviews()
    total_score = 0
    count = 0
    for interview in interviews:
        if interview != "":
            interview_data = eval(interview) #converting the string representation of the dictionary back to a dictionary
            total_score += interview_data[metric_name]
            count += 1
    if count > 0:
        average_score = total_score / count
        return average_score
    else:
        return 0
    
#This function will count the number of interviews conducted by reading the "interviews.txt" file and counting the number of lines in the file.
# We will subtract 1 from the count to account for the footer empty line in the file. The text file has no header line, so we will count all lines in the file and subtract 1 to get the total number of interviews conducted. The function takes the filename as an argument and returns the count of interviews.
def count_interviews(filename):
    interviews = get_all_interviews()
    return len(interviews) - 1

#loading the interviews
def load_data(filename):
    file = open(filename, "r")
    data = file.read()
    file.close()
    return data

#saving the interviews
def save_data(data, filename):
    file = open(filename, "a")
    file.write(str(data) + "\n")
    file.close()

#added menu system where the user asks if they want to add another interview or view all interviews or exit the program
def start_menu():
    while True:
        print("-------------------------------")
        print("\nPlease select an option from below:")
        print("1. Add a new interview")
        print("2. View all interviews conducted")
        print("3. View market insights and analysis")
        print("4. View Ideal Customer Profile (ICP) Summary")
        print("5. View Ranked Prospects")
        print("6. Exit the program")
        choice = input("\nEnter your choice between (1/2/3/4/5/6): ")
        if choice == "1":
            customer = add_interview()
            save_data(customer, "interviews.txt")
            print("\nInterview added successfully!")
        elif choice == "2":
            all_interviews = load_data("interviews.txt")
            print("\nAll Interviews data are as follows:")
            print(all_interviews)
            print(f"\nTotal interviews conducted: {count_interviews('interviews.txt')}")
        elif choice == "3":
            print("\nMarket Insights and Analysis:")
            print('---------------------------------')
            print(f"Importance Score: {calculate_average('importance_score')}")
            print(f"\nEffort Score: {calculate_average('effort_score')}")
            print(f"\nCost Concern Score: {calculate_average('cost_concern')}")
            print(f"\nTech Interest Score: {calculate_average('tech_interest')}")
            print(f"\nFacility Size Distribution: {get_facility_size_distribution()}")
            print(f"\nPilot Readiness Count: {calculate_pilot_ready_count()} out of {count_interviews('interviews.txt')}")
            print(f"\nPilot Readiness Percentage: {pilot_readiness_percentage():.2f}%")
        elif choice == "4":
            print('---------------------------------')
            display_icp_summary()
        elif choice == "5":
            #print("\nRanked Prospects are as follows:")
            print("\nProspect Prioritization Summary Report is as follows:")
            print('---------------------------------')
            prospect_summary = generate_prospect_summary()
            print(f"\nTotal Prospects: {prospect_summary['total_prospects']}")
            print(f"\nHigh Priority (Tier 1 ICP): {prospect_summary['high_priority']}")
            print(f"\nMedium Priority (Tier 2 ICP): {prospect_summary['medium_priority']}")
            print(f"\nLow Priority (Not ICP): {prospect_summary['low_priority']}")
            print(f"\nTop Prospect: {prospect_summary['top_prospect']}")
            display_prospect_rankings()
        elif choice == "6":
            print("Exiting the program. Visit again!")
            break
        else:
            print("Invalid choice of options. Please try again.")

def add_interview():
    #These are the fields that we will be asking the user to fill in for each customer interview. We will store these values in a dictionary called "customer". The keys of the dictionary will be the field names and the values will be the user input. We will then return this dictionary at the end of the function.
    # customer = {
    #"organization_name": "",
    #"organization_type": "",
    #"facility_size": "",
    #"importance_score": 0,
    #"effort_score": 0,
    #"cost_concern": 0,
    #"tech_interest": 0,
    #"pilot_readiness": "",
    #"comment":}

#asking the user for Organization Name
    organization_name = input("Enter your Organization Name: ")
    print("You entered Organization Name:", organization_name)

#asking the user for Organization Type    
    organization_type = input("Enter your Organization Type (e.g.Facility Management, Sustainability / ESG, Operations, Administration, Procurement, Finance, Other): ")
    print("You entered Organization Type:", organization_type)
#asking the user for Facility Size
    facility_size = input("Enter your Facility Size (<100, 100 to 500, 501 to 2000, 2001 to 10000, 10000+, Unknown): ")
    print("You entered Facility Size:", facility_size)
#asking the user for Importance Score 
    importance_score = int(input("Importance Score for Waste Segregation on a scale of 1-10: "))
    print("You entered Importance Score:", importance_score)
    
#asking the user for Effort Score
    effort_score = int(input("Effort Score for Waste Segregation on a scale of 1-10: "))
    print("You entered Effort Score:", effort_score)

#asking the user for Cost Concern Score
    cost_concern = int(input("Cost Concern Score for Waste Segregation on a scale of 1-10: "))
    print("You entered Cost Concern Score:", cost_concern)

#asking the user for Tech Interest Score
    tech_interest = int(input("Tech Interest Score for Waste Segregation on a scale of 1-10: "))
    print("You entered Tech Interest Score:", tech_interest)

#asking the user for Pilot Readiness
    pilot_readiness = input("Are you ready for a pilot program with our solution that can solve your waste segregation challenges? (Yes/No): ")
    print("You entered Pilot Readiness:", pilot_readiness)

#asking the user for any additional comments
    comment = input("Any additional comments or insights you'd like to share about your waste management challenges and needs? ")
    print("You entered Comment:", comment)

#creating a customer dictionary to store the values given by the user
    customer = {
    "organization_name": organization_name,
    "organization_type": organization_type,
    "facility_size": facility_size,
    "importance_score": importance_score,
    "effort_score": effort_score,
    "cost_concern": cost_concern,
    "tech_interest": tech_interest,
    "pilot_readiness": pilot_readiness,
    "comment": comment
}
    return customer



if __name__ == "__main__":
    main()
    
