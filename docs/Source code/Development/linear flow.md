This doc describes what Linear is and how to use it when working on the Cob project.
#### What is Linear? 
Linear is an issue tracker web app. It can create issues, which have various bits of information about them. They can be ordered, filtered, etc. We'll be using it for the project.

#### What are the things in linear?
The units in Linear are: Workspace, Team, Project, Issue. We have the workspace 'KC-juniors-cob', which has the team 'Main team', and which team has the project 'COB project'.
Issues belong to a team, and for our needs, all issues will belong to the COB project as well.

There are 3 buttons to remember:
Under Main team, they are
- Issues
- Active
- Backlog
Issues - all issues, with a kanban style view set as default (can be customized from 'Display')
Active - issues that are either marked TODO or In Progress ([[#What is in each issue?|Statuses bellow]]), in a list
Backlog - issues marked Backlog, in a list

You can also filter them from the 'Filter' button.
#### What is in each issue?
Each issue has a few important bits of info:
- Title: 
	The name of the issue
- Description:
	A more verbose description of what it is
- Status:
	 The little circle next to its title. It can be: Backlog (perforated circle), TODO (white circle), In progress (yellow circle), Done (blue with check mark) or canceled/duplicate (with an X)  
- Priority:
	 The network-esque bars, either 3, 2, or 1 bar to denote priority, '!' for 'urgent' and '...' for 'no priority' (i.e. should be assigned)
- Sub-tasks:
	 Tasks can be given sub-tasks. When they have such sub-tasks, they get a n/m (n sub-tasks Done out of 'm' total) indicator. Sub-tasks act as any other task, and can also be hidden from 'Display' 
- Assignee:
	 List of people assigned to the task
- History/Comments:
	 Whatever there is to comment on the issue, and historic changes (created, status changed, renamed, etc.)
#### What do i do?
When an issue arises - create it in Linear (with the little pen button in the top left). When its finished - mark it as such. Chose tasks that are TODO, and after that move tasks based either on priority or relevance from Backlog to TODO.