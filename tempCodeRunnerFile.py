     # Καταχώρηση ψεύτικων εσόδων εάν δεν υπάρχουν
    if len(dbin.showData('income'))<1:
        for i in income_examples:
            dbin.InsertIncome(i['name'], 
                            i['amount'], 
                            return_index(i['category'], dbin.showData('category_table', dataframe=False)), 
                            i['date'], 
                            random.randint(0, 2))
    
    # Καταχώρηση ψεύτικων εξόδων εάν δεν υπάρχουν
    if len(dbin.showData('expenses'))<1:
        for i in expense_examples:
            dbin.InsertExpense(i['name'], 
                            i['amount'], 
                            return_index(i['category'], dbin.showData('category_table', dataframe=False)), 
                            i['date'], 
                            random.randint(0, 2))