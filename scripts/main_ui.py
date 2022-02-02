#! /usr/bin/env python

# Import libraries
import rospy
import time
import os

# Messages
from std_srvs.srv import Empty
from move_base_msgs.msg import MoveBaseActionFeedback
from move_base_msgs.msg import MoveBaseActionGoal
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from actionlib_msgs.msg import GoalID


# Constant
# Threshold for reaching the goal
th_reach = 0.3
# Threshold for avoiding collision
th_collision = 0.7
# Max time to let the robot reach the target is 2 minutes
max_time = rospy.Duration(120)
# Initialize input for manual driving mode
input_man = 'a'
# Starting without a goal
goal_set = False
# Define vel_msg 
vel_msg = Twist()


'''
   Function to print on screen the options which the user can choose from 
'''
def print_ui():
    # User Interface
    print('Type commands on keyboard to decide the robot driving mode:\n\n')
    print('1: Autonomus drive setting a goal point using (x,y) coordinates\n')
    print('2: Manual driving mode using the keyboard to control the robot\n')
    print('3: Assisted manual driving mode using the keyboard to control the robot\n')
    print('4: Delete the current goal expressed by (x,y)\n')
    print('9: Reset robot position\n\n')
    print('0: EXIT THE PROGRAM\n\n')


''' 
   Function that checks the user's input from keyboard and returns it 
 
   @return int, user's input
'''
def check_user_input():
    # Getting input from user, it must be integer
    while True:
        try:
            # if input can be converted to an integer it exit from the while
            user_choice = int(input('Command from user: '))
            break
        except:
            print('Please, type an integer number')
    
    return user_choice


'''
   Function used to print the goal given from user once is set
'''
def print_goal():
    if goal_set:
        print('The goal has been given by user!\n\n')
        print('Goal:  x = %.2f   y = %.2f\n\n' % (goal_x, goal_y))
        print('Robot will try to reach autonomusly the goal\n')
    else:
        print('Goal has not been set yet\n\n')


'''
   Function that set the objective (point in space) that the robot
   needs to reach autonomusly
'''
def set_goal():
    global goal_set, start_time
    # Clear terminal
    os.system('clear')
    # Ask the goal's x-coordinate to the user, it must be float
    while True:
        try:
            # if input can be converted to a floating number it exit from the while
            in_x = float(input('\nPlease, type the x-coordinate for the goal: '))
            break
        except:
            print('Please, type a number')

    # Ask the goal's y-coordinate to the user, it must be float
    while True:
        try:
            # if input can be converted to a floating number it exit from the while
            in_y = float(input('\nPlease, type the y-coordinate for the goal: '))
            break
        except:
            print('Please, type a number')

    # initialize the goal given by user
    goal_msg = MoveBaseActionGoal()

    goal_msg.goal.target_pose.header.frame_id = "map"
    goal_msg.goal.target_pose.pose.orientation.w = 1

    goal_msg.goal.target_pose.pose.position.x = in_x
    goal_msg.goal.target_pose.pose.position.y = in_y

    # publish goal message and get the time
    pub_goal.publish(goal_msg)
    start_time = rospy.Time.now()

    # goal has been set
    goal_set = True


'''
   Function used to store the goal once it is published

   @param msg, goal subscribed by move_base topic
'''
def get_goal(msg):
    global goal_x, goal_y
    goal_x = msg.goal.target_pose.pose.position.x
    goal_y = msg.goal.target_pose.pose.position.y


'''
   Function that tells if the goal has been reached, prints a message and cancel the goal
   A goal is considered to be unreachable if after five minutes the robot don't arrive to
   the goal
   The function is called each time 

   @param msg, actual goal
'''
def goal_reached(msg):
    global goal_set
    if goal_set:
        # Get time
        end_time = rospy.Time.now()
        goal_time = end_time - start_time
        # If time expired, target can not be reached
        if goal_time > max_time:
            cancel_goal()
            print('TIME EXPIRED: target is considered unreachable\n\n')
            time.sleep(1)
            
        # Get robot position in a certain instant
        rob_x = msg.feedback.base_position.pose.position.x
        rob_y = msg.feedback.base_position.pose.position.y

        # See how far the robot is from the goal
        x_dist = rob_x - goal_x
        y_dist = rob_y - goal_y

        # See if it's close enough to be considered goal reached
        if abs(x_dist) < th_reach and abs(y_dist) < th_reach:
            cancel_goal()
            print('GOAL REACHED\n\n') 
            time.sleep(1)      
	    

'''
   Function used to cancel the goal
'''
def cancel_goal():
    global goal_set
    # No goal has been set
    if not goal_set:
        print('\nThere is no goal to cancel!\n\n')
        time.sleep(2)
     # If there is a goal, cancel it
    else:
        # cancel_msg.id = id
        cancel_msg = GoalID()
        pub_canc.publish(cancel_msg)
        goal_set = False
        print('\nGoal has been canceled!!!\n\n')
        time.sleep(2)


'''
   Function used to let the user acquire the control of the robot
   The aim is to allow to control the robot's movements using the keyboard
'''
def manual_driving():
    global input_man
    os.system('clear')
    while input_man != 'b':
        # Print the selected manual mode
        if drive_assistance:
            print('\nManual mode drive assistance active\n\n')
        else:
            print('\nManual mode drive assistance NOT active\n\n')
        # Get input for exiting from manual mode
        while True:
            try:
                # if waits an input from user
                input_man = input('Press:\nb ---> back to main menu\n')
                break
            except:
                print('Please, choose a char\n')

        # Before exiting the manual mode i need to stop the robot
        if input_man == 'b':
            print('\nEXITING the manual mode\n')
            # Set velocity to zero
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            # Publish the velocity
            pub_vel.publish(vel_msg)
        else:
            print('Please, type: b to go back to main menu\n')
    # Setting input_man with something different from 'b' before exiting
    input_man = 'a' 

'''
   Function called each time arrives a message from the LaserScan topic
   If the user asks for driving assistance while it's in manual mode the 
   funcion gets the min value among a region of the laser scan and take a decision
   to avoid obstacles
   If user doesn't sk for assistance, the function does nothing

   @param msg, array of values given by /scan topic
'''
def assisted_driving(msg):
    global regions, vel_msg
    # If no assistance is required, exit the function
    if not drive_assistance:
        return
    # If assistance is enabled, help the user driving around
    else:
    
        regions = {
            'right':  min(min(msg.ranges[0:143]), 10),
            'fright': min(min(msg.ranges[144:287]), 10),
            'front':  min(min(msg.ranges[288:431]), 10),
            'fleft':  min(min(msg.ranges[432:575]), 10),
            'left':   min(min(msg.ranges[576:719]), 10),
        }
        # Avoid risky situations when the robot is going to collide into walls
        # Ostacle positioned in front of the robot
        if regions['front'] < th_collision:
            # Allow only rotation
            if vel_msg.linear.x > 0 and vel_msg.angular.z == 0:
                # Stop robot's linear velocity
                vel_msg.linear.x = 0

        # Ostacle positioned on the front-right of the robot    
        elif regions['fright'] < th_collision:
            # Allow only rotation on the left
            if vel_msg.linear.x > 0 and vel_msg.angular.z < 0:
                # Stop robot's linear velocity
                vel_msg.linear.x = 0
                vel_msg.angular.z = 0

        # Ostacle positioned on the front-left of the robot
        elif regions['fleft'] < th_collision: 
            # Allow only rotation on the right
            if vel_msg.linear.x > 0 and vel_msg.angular.z > 0:
                # Stop robot's linear velocity
                vel_msg.linear.x = 0
                vel_msg.angular.z = 0

        # Ostacle positioned on the right of the robot
        elif regions['right'] < th_collision:
            # Allow only rotation on the left
            if vel_msg.linear.x == 0 and vel_msg.angular.z < 0:
                # Stop robot's linear velocity
                vel_msg.linear.x = 0
                vel_msg.angular.z = 0

        # Ostacle positioned on the left of the robot
        elif regions['left'] < th_collision: 
            # Allow only rotation on the right
            if vel_msg.linear.x == 0 and vel_msg.angular.z > 0:
                # Stop robot's linear velocity
                vel_msg.linear.x = 0
                vel_msg.angular.z = 0
        
        # Set new velocity and publish it
        pub_vel.publish(vel_msg)

'''
   Function called each time the user uses the teleop keyboard to change the
   robot's velocity

   @param 
'''
def set_user_vel(msg):
    global vel_msg
    # If the robot is not in manual mode, the command given from user is ignored
    if not man_mode:
    	return
    else:
    	# If the robot is not in drive assistance mode, the velocity is published
    	if not drive_assistance:
    		pub_vel.publish(msg)
    		return
    	# If the robot is in manual mode and the drive assistance is active the message 
    	# given by user is saved and checked from the assisted driving function
    	else:
    		vel_msg.linear.x = msg.linear.x
    		vel_msg.angular.z = msg.angular.z    		
     

''' 
   Function used to decide the behavior of the robot according to 
   the user input
 
   @param input_u, user's input
'''
def driving_decision(input_u):
    global man_mode, drive_assistance
    # Select what to do
    # Autonomus driving with goal set from user
    if input_u == 1:
        # setting the goal that user wants to reach
        set_goal()
        if goal_set:
            os.system('clear')
            # Print on screen the goal
            print_goal()
            # Allow user to see what is the goal
            time.sleep(5)

    # Manual driving mode
    elif input_u == 2:
        # Manual mode activated
        man_mode = True
        # No assistance
        drive_assistance = False
        manual_driving()
        # Exit from manual mode
        man_mode = False

    # Assisted manual driving mode
    elif input_u == 3:
        # Manual mode activated
        man_mode = True
        # Assistance needed
        drive_assistance = True
        manual_driving()
        # Set driving assistance to false
        drive_assistance = False
        # Exit from manual mode
        man_mode = False

    # Cancel robot position 
    elif input_u == 4:
    	cancel_goal()
    	print('Goal canceled!') # Feeback to user
    
    # Reset robot position
    elif input_u == 9:
        reset_world()
        print('Reset environment!\n')  # Feedback to user

    # Exit the loop
    elif input_u == 0:
        # Clear terminal
        os.system('clear')
        # Calling function for UI 
        print('Program is EXITING')
        # Kill all the nodes
        rospy.on_shutdown()

    # Not one of the possible options  
    else:
        # Clear terminal
        os.system('clear')
        print('Invlid input.\nPlease, type one of the following:\n\n')
        print_ui()
        

''' main function '''
def main():
    # initialize global variables
    global goal_set, drive_assistance, man_mode, input_u, goal_to_cancel
    global pub_goal, pub_vel, pub_canc, sub_laser, sub_goal, sub_user_vel, sub_robot_pos, reset_world

    # Initialize that the goal has not been set yet
    goal_set = False
    # Initialize that there is no need of driving assistence
    drive_assistance = False
    # Initialize that the robot is not in manual mode
    man_mode = False

    # Initialize the node, setup the NodeHandle for handling the communication with the ROS system  
    rospy.init_node('main_ui')

    # Create a client to reset the simulation environment
    rospy.wait_for_service('/gazebo/reset_world')
    reset_world = rospy.ServiceProxy('/gazebo/reset_world', Empty)

    # Initialize publishers
    pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=100)
    pub_goal = rospy.Publisher('move_base/goal', MoveBaseActionGoal, queue_size=100)
    pub_canc = rospy.Publisher('move_base/cancel', GoalID, queue_size=100)

    # Initialize subscribers
    sub_laser = rospy.Subscriber('/scan', LaserScan, assisted_driving)
    sub_goal = rospy.Subscriber('move_base/goal', MoveBaseActionGoal, get_goal)
    sub_user_vel = rospy.Subscriber('/us_cmd_vel', Twist, set_user_vel)
    sub_robot_pos = rospy.Subscriber('move_base/feedback', MoveBaseActionFeedback, goal_reached)

    # Infinite loop until user doesn't press 9 and ros::ok() returns true
    while not rospy.is_shutdown():
        # Print ui
        print_ui()
        # Get input from user
        input_u = check_user_input()
        # Decide what to do based on user decision
        driving_decision(input_u)


if __name__ == '__main__':
    main()