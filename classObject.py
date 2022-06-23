from data import UserGroup
from expense_calculator import minCashFlow
from flask import request

groups = []


class ExpenseTracker():

    def post(self,group_name):

        """
            It adds new expenses to the group with a name.
        """

        data = request.json

        members = []

        for item in data["items"]:
            for member in item['paid_by'][0]:
                members.append(member)

            for member in item['owed_by'][0]:
                members.append(member)

        #It checks for an existing expenses name and adds it to the dictionary if not

        for group in groups:
            if group.name == group_name:
                for expense in group.expenses:
                    if expense['name'] == data['name']:
                        return {"msg": "Expense with name already exists"}

                group.add_expense(data)
                group.set_members(set(members))
                return {"method ": "Expense added successfully"}

        return {"method ": "Group does not exist"}

    def put(self, group_name):

        """
            It updates new expenses to the group with a name..
        """

        data = request.json

        members = []

        for item in data['items']:
            for member in item['paid_by'][0]:
                members.append(member)

            for member in item['owed_by'][0]:
                members.append(member)

        for group in groups:
            if group.name == group_name:
                for expense in group.expenses:
                    if expense['name'] == data['name']:
                        expense = data
                        group.set_members(set(members))
                        return {"msg": "Expense updated successfully."}

                return {"msg": "Expense does not exist."}

        return {"method ": "Group does not exist"}

    def delete(self, group_name, expense_name):

        """
            It deletes expenses to the group with a name.
        """

        data = request.json

        for group in groups:
            if group.name == group_name:
                for index in range(len(group.expenses)):
                    if group.expenses[index]['name'] == expense_name:
                        del group.expenses[index]
                        return {"msg": "Expense deleted successfully."}

                return {"msg": "Expense does not exist."}

        return {"method ": "Group does not exist"}



class GroupTracker():

    def get(self,group_name):

        for group in groups:
            if group.name == group_name:

                if not group.expenses:
                    return {"method ": "No expense in group."}

                members = list(group.members)
                graph = [[0 for x in range(len(members))] for y in range(len(members))]
                debt = [[0 for x in range(len(members))] for y in range(len(members))]
                balances = {}

                for expense in group.expenses:
                    for item in expense["items"]:
                        paid_by = item["paid_by"][0].copy()
                        owed_by = item["owed_by"][0].copy()

                        for key1, value1 in paid_by.items():
                            for key, value in owed_by.items():
                                if owed_by[key]:
                                    mn = min(value1, value)
                                    paid_by[key1] -= mn
                                    owed_by[key] -= mn

                                    if not key1 == key:
                                        graph[members.index(key)][members.index(key1)] += mn

                                    if not paid_by[key1]:
                                        break

                    minCashFlow(graph, len(members), debt)

                    for i in range(len(members)):
                        total = 0
                        owes_to = []
                        owed_by = []

                        for j in range(len(members)):

                            if debt[i][j] != 0:
                                total -= debt[i][j]
                                owes_to.append({members[j]: debt[i][j]})

                            if debt[j][i] != 0:
                                total += debt[j][i]
                                owed_by.append({members[j]: debt[j][i]})

                        balances[members[i]] = {
                            "total_balance": total,
                            "owes_to": owes_to,
                            "owed_by": owed_by
                        }

                return {
                    "name": group_name,
                    "balances": balances
                    }

        return {"method ": "Group does not exist"}

    def post(self, request):

        data = request.json


        for group in groups:
            if group.name == data['name']:
                return {"msg": "Group already exists."}

        groups.append(UserGroup(data['name'], data['members']))

        return {"msg": "Group created successfully."}
