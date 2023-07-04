leaves = Leave.objects.filter(employee = emp_to_pay,status='accepted').count()

                holiday_dates = []
                holidays = Holidays.objects.filter(month=selected_month)
                for holidays in holidays:
                    holiday_dates.append(holidays.holiday)

                
                salary=emp_to_pay.emp_salary


                
                if salary <= 41666.66:
                    tax_deduction = salary * 0.01
                elif salary <= 58333.33:
                    tax_deduction = 500 + (salary - 41666.66) * 0.1
                elif salary <= 83333.33:
                    tax_deduction = 2500 + (salary - 58333.33) * 0.2
                elif salary <= 166666.67:
                    tax_deduction = 6500 + (salary - 83333.33) * 0.3
                else:
                    tax_deduction = 24166.67 + (salary - 166666.67) * 0.36



                advance_this_month =0
                advance_obj = Salary.objects.filter(employee = emp_to_pay,type='advance',month=selected_month)
                for adv in advance_obj:
                    advance_this_month = advance_this_month + adv.paid_salary
                final_salary = salary-tax_deduction-advance_this_month
                salary_status = Salary.objects.filter(employee = emp_to_pay,month=selected_month,type='salary')
                if salary_status:
                    status='paid'
                else:
                    status='unpaid'
                
                data_list.append({
                    'emp_id':emp_to_pay,
                    'month':selected_month.month,
                    'employee':str(emp_to_pay.user.first_name +' '+ emp_to_pay.user.last_name),
                    'salary':salary,
                    'final_salary':final_salary,
                    'tax_deduction':tax_deduction,
                    'status':status,
                    'advance_this_month':advance_this_month
                })