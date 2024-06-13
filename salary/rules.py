from salary.models import *

def calc_base_salary_coefficient(employee, effective_process):
    try:
        std_salary = StdSalary.objects.get(employee=employee)
        return std_salary.base_salary_coefficient
    except StdSalary.DoesNotExist:
        raise AttributeError("Missing information base salary coefficient")
    
def calc_base_salary(employee, effective_process):
    try:
        return employee.position.base_salary
    except AttributeError:
        raise AttributeError("Employee does not have a position")
    


def calc_social_security_salary(employee, effective_process):
    try:
        ss_base_self_declare = SocialSecurityProvidentFund.objects.get(employee=employee).social_security_base_self_declare
        if ss_base_self_declare == 0:
            return 0, 0, 0
        salary_rule = SalaryRule.objects.get(company=employee.company)
        ss_company_bear_base = salary_rule.social_security_company_bear_base
        ss_company_rate = salary_rule.social_security_company_rate
        ss_self_rate = salary_rule.social_security_self_rate

        ss_amount_self_declare = ss_base_self_declare * ss_self_rate / 100
        ss_amount_company_bear = ss_company_bear_base * ss_company_rate / 100
        ss_additional_amount_self_bear = (ss_base_self_declare - ss_company_bear_base) * ss_company_rate / 100
        #个人申报, 公司承担, 个人额外承担
        return ss_amount_self_declare, ss_amount_company_bear, ss_additional_amount_self_bear
    except (StdSalary.DoesNotExist, Attendance.DoesNotExist, SocialSecurityProvidentFund.DoesNotExist, SalaryRule.DoesNotExist):
        return 0, 0, 0
        # raise AttributeError("Missing information for salary calculation")

def calc_provident_fund_salary(employee, effective_process):
    try:
        pf_base_self_declare = SocialSecurityProvidentFund.objects.get(employee=employee).provident_fund_base_self_declare
        if pf_base_self_declare == 0:
            return 0, 0, 0
        salary_rule = SalaryRule.objects.get(company=employee.company)
        pf_company_bear_base = salary_rule.provident_fund_company_bear_base
        pf_company_rate = salary_rule.provident_fund_company_rate
        pf_self_rate = salary_rule.provident_fund_self_rate

        pf_amount_self_declare = pf_base_self_declare * pf_self_rate / 100
        pf_amount_company_bear = pf_company_bear_base * pf_company_rate / 100
        pf_additional_amount_self_bear = (pf_base_self_declare - pf_company_bear_base) * pf_company_rate / 100
        return pf_amount_self_declare, pf_amount_company_bear, pf_additional_amount_self_bear
    except (StdSalary.DoesNotExist, Attendance.DoesNotExist, SocialSecurityProvidentFund.DoesNotExist, SalaryRule.DoesNotExist):
        return 0, 0, 0
        # raise AttributeError("Missing information for salary calculation")
    
def calc_std_salary(employee, effective_process):
    try:
        base_salary = employee.position.base_salary # employee must have a position
        base_salary_coefficient = StdSalary.objects.get(employee=employee).base_salary_coefficient
        standard_salary = base_salary * base_salary_coefficient
        return standard_salary
    except AttributeError:
        raise AttributeError("Employee does not have a position")
    
def calc_std_ensured_salary(employee, effective_process):
    try:
        return employee.position.ensure_salary
    except AttributeError:
        raise AttributeError("Employee does not have a position")


def calc_std_merit_salary(employee, effective_process):
    return calc_std_salary(employee, effective_process) - calc_std_ensured_salary(employee, effective_process)


def calc_attendance_deduction(employee, effective_process):
    try: # TODO: 迟到早退扣款 + 缺卡缺勤扣款
        deduction = 0
        # attendance = Attendance.objects.get(employee=employee)
        # std_salary = StdSalary.objects.get(employee=employee)
        # late_times = attendance.late_times
        # early_leave_times = attendance.early_leave_times
        # punch_in_missing_times = attendance.punch_in_missing_times
        # punch_out_missing_times = attendance.punch_out_missing_times
        # absent_times = attendance.absent_times

        # if late_times + early_leave_times > 3:
        #     deduction += 100 * (late_times + early_leave_times - 3)
        # deduction += ((punch_in_missing_times + punch_out_missing_times) / 2 + absent_times) * std_salary.std_salary / 21.75
        return deduction
    except (StdSalary.DoesNotExist, Attendance.DoesNotExist):
        raise AttributeError("Missing information for Attendancy Deduction calculation")
    
def calc_assessment_increase(employee, effective_process):
    try:
        salary_adj = SalaryAdjustment.objects.filter(employee=employee,
                                                    direction='I',
                                                    adjustment_type = 'A',
                                                    effective_process=effective_process)
        assessment_increase = 0
        for adj in salary_adj:
            assessment_increase += adj.amount
        return assessment_increase
    except SalaryAdjustment.DoesNotExist:
        return 0
    
def calc_assessment_decrease(employee, effective_process):
    try:
        salary_adj = SalaryAdjustment.objects.filter(employee=employee,
                                                    direction='D',
                                                    adjustment_type = 'A',
                                                    effective_process=effective_process)
        assessment_decrease = 0
        for adj in salary_adj:
            assessment_decrease += adj.amount
        return assessment_decrease
    except SalaryAdjustment.DoesNotExist:
        return 0
    
def calc_illness_leave_deduction(employee, effective_process):
    raise NotImplementedError

def calc_no_salary_leave_deduction(employee, effective_process):
    # TODO: not checked 病假扣款 + 事假扣款
    try:
        deduction = 1
        # attendance = Attendance.objects.get(employee=employee)
        # no_salary_leave_duration = attendance.no_salary_leave_duration
        # deduction += no_salary_leave_duration / 8 * calc_std_salary(employee, effective_process) / 21.75
        return deduction
    except (Attendance.DoesNotExist):
        raise AttributeError("Missing information for No Salary Leave Deduction calculation")


def calc_salary_increase(employee, effective_process):
    try:
        salary_increase = 0
        salary_adj = SalaryAdjustment.objects.filter(employee=employee, 
                                                  direction='I', 
                                                  adjustment_type = 'I', 
                                                  effective_process=effective_process)
        for adj in salary_adj:
            salary_increase += adj.amount
        return salary_increase
    except SalaryAdjustment.DoesNotExist:
        return 0

def calc_salary_decrease(employee, effective_process):
    try:
        salary_decrease = 0
        salary_adj = SalaryAdjustment.objects.filter(employee=employee,
                                                  direction='D',
                                                  adjustment_type = 'I',
                                                  effective_process=effective_process)
        for adj in salary_adj:
            salary_decrease += adj.amount
        return salary_decrease
    except SalaryAdjustment.DoesNotExist:
        return 0

def calc_total_salary(employee, effective_process):
    try:
        total_salary = calc_std_salary(employee, effective_process) + calc_salary_increase(employee, effective_process) - calc_salary_decrease(employee, effective_process) - calc_no_salary_leave_deduction(employee, effective_process)
        return total_salary
    except (StdSalary.DoesNotExist, AttributeError):
        raise AttributeError("Missing information for Total Salary calculation")
    
def calc_meal_subsidy(employee, effective_process):
    # TODO: not checked
    try:
        meal_subsidy = 0
        # attendance = Attendance.objects.get(employee=employee, effective_process=effective_process)
        # meal_subsidy_plan = StdSalary.objects.get(employee=employee).meal_subsidy_plan
        # meal_subsidy = meal_subsidy_plan * attendance.work_days
        return meal_subsidy
    except (StdSalary.DoesNotExist, Attendance.DoesNotExist):
        raise AttributeError("Missing information for Meal Subsidy calculation")


def calc_weather_subsidy(employee, effective_process):
    raise NotImplementedError

def calc_other_subsidy(employee, effective_process):
    try:
        salary_adj = SalaryAdjustment.objects.filter(employee=employee,
                                                    direction='I',
                                                    adjustment_type = 'S',
                                                    effective_process=effective_process)
        other_subsidy = 0
        for adj in salary_adj:
            other_subsidy += adj.amount
        return other_subsidy
    except SalaryAdjustment.DoesNotExist:
        return 0

def calc_total_subsidy(employee, effective_process):
    return calc_meal_subsidy(employee, effective_process) + calc_other_subsidy(employee, effective_process)

def calc_salary_before_assessment(employee, effective_process):
    return calc_total_salary(employee, effective_process) + calc_total_subsidy(employee, effective_process)

def calc_other_assessment_increase(employee, effective_process):
    raise NotImplementedError

def calc_total_salary_before_tax_and_fee(employee, effective_process):
    return calc_salary_before_assessment(employee, effective_process) - calc_assessment_decrease(employee, effective_process) + calc_assessment_increase(employee, effective_process) 

def calc_social_security_provident_fund_self_bear(employee, effective_process):
    _, _, ss_additional_amount_self_bear = calc_social_security_salary(employee, effective_process)
    _, _, pf_additional_amount_self_bear = calc_provident_fund_salary(employee, effective_process)
    return ss_additional_amount_self_bear + pf_additional_amount_self_bear

def calc_total_salary_for_tax_calc(employee, effective_process):
    try:
        return calc_total_salary_before_tax_and_fee(employee, effective_process) - calc_social_security_provident_fund_self_bear(employee, effective_process)
    except StdSalary.DoesNotExist:
        raise AttributeError("Missing information for Total Salary for Tax calculation")


def calc_fee_self_bear(employee, effective_process): # 个人承担(社保 + 公积金)+工会费(=工会费率*total_salary*is_labor_union_member)
    try:
        ss_self_declare, _, _ = calc_social_security_salary(employee, effective_process)
        pf_self_declare, _, _ = calc_provident_fund_salary(employee, effective_process)
        salary_rule = SalaryRule.objects.get(company=employee.company)
        return ss_self_declare + pf_self_declare + salary_rule.labor_union_fee_self_rate * calc_total_salary(employee, effective_process) * employee.in_labour_union_member / 100
    except SalaryRule.DoesNotExist:
        raise AttributeError("Missing information for Fee Self Bear calculation")

def calc_tax_self_bear(employee, effective_process):
    # TODO: Wrong function. add tax table
    return 1


def calc_total_salary_after_tax(employee, effective_process):
        return calc_total_salary_for_tax_calc(employee, effective_process) - calc_tax_self_bear(employee, effective_process) - calc_fee_self_bear(employee, effective_process)

def calc_increase_after_tax(employee, effective_process):
    try:
        salary_adj = SalaryAdjustment.objects.filter(employee=employee,
                                                    direction='I',
                                                    adjustment_type = 'T',
                                                    effective_process=effective_process)
        increase_after_tax = 0
        for adj in salary_adj:
            increase_after_tax += adj.amount
        return increase_after_tax
    except SalaryAdjustment.DoesNotExist:
        return 0
    
def calc_decrease_after_tax(employee, effective_process):
    try:
        salary_adj = SalaryAdjustment.objects.filter(employee=employee,
                                                    direction='D',
                                                    adjustment_type = 'T',
                                                    effective_process=effective_process)
        decrease_after_tax = 0
        for adj in salary_adj:
            decrease_after_tax += adj.amount
        return decrease_after_tax
    except SalaryAdjustment.DoesNotExist:
        return 0
    