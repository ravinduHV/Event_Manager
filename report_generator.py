from fpdf import FPDF
from cs50 import SQL

db = SQL("sqlite:///manager.db")


class generate_pdf_report():
    def __init__(self, lable, orientation=2, font_size=2):
        self.orientation = orientation
        self.font_size = font_size
        if len(lable) == 0:
            lable = "User-System:Request[200]"
        self.lable = lable
    
    def __str__(self):
        return f"{self.orientation}, {self.font_size}, {self.lable}"

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, option):
        match option:
            case 1:
                self._orientation = "portrait"
            case 2:
                self._orientation = "landscape"
            case _:
                self._orientation = "landscape"

    @property
    def font_size(self):
        return self._font_size
    
    @font_size.setter
    def font_size(self, option):
        match option:
            case 1:
                self._font_size = 8
            case 2:
                self._font_size = 9
            case 3:
                self._font_size = 10
            case 4:
                self._font_size = 12
            case _:
                self._font_size = 10
    
    def budget_report(self, id):
        details = db.execute("SELECT * FROM events WHERE id=?", id)
        income = db.execute("SELECT * FROM budget_income WHERE project_id=?",id)
        expends = db.execute("SELECT * FROM budget_expenditure WHERE project_id=?",id) 

        pdf = FPDF(orientation=self.orientation, format="A4")
        pdf.set_font_size(11)
        pdf.add_page()

        html = f"""
                <table border="1" style=" border-collapse: collapse; text-align:center;" ><thead>
		        <tr>
                    <th width="7%">Date</th>
                    <th width="7%">Catagory</th>
                    <th width="17%">Description [INCOME]</th>
                    <th width="3%">Units</th>
                    <th width="6%">Unit Price</th>
                    <th width="10%">Amount</th>

                    <th width="7%">Date</th>
                    <th width="7%">Catagory</th>
                    <th width="17%">Description [EXPENDS]</th>
                    <th width="3%">Units</th>
                    <th width="6%">Unit Price</th>
                    <th width="10%">Amount</th>
                </tr>
                </thead>
                <tbody>"""
        income_l, expends_l = len(income), len(expends)
        if income_l < expends_l:
            length = expends_l
        else:
            length = income_l 
        
        print(length)
        
        for _ in range(length):
            line=""
            try:
                row1 = income[_]
                line += f"""<tr style="text-align:right;">
                            <td>{row1['date']}</td>
                            <td>{row1['type']}</td>
                            <td>{row1['item']}</td>
                            <td>{row1['units']}</td>
                            <td>{row1['amount']}</td>
                            <td>{float(row1['units'])*float(row1['amount']) }</td>"""
                
            except:
                line += f"""<tr>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>"""
            try:
                row2 = expends[_]
                line += f"""
                            <td>{row1['date']}</td>
                            <td>{row1['type']}</td>
                            <td>{row1['item']}</td>
                            <td>{row1['units']}</td>
                            <td>{row1['amount']}</td>
                            <td>{float(row1['units'])*float(row1['amount']) }</td>
                            </tr>"""
            except:
                line += f"""
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td></tr>"""
            html = html + line 
        html = html + """</tbody></table>"""
             
        pdf.write_html(html , table_line_separators=True)
        pdf.output('table_html.pdf')

        print(details)
        print(income)
        print(expends)