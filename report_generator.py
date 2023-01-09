from fpdf import FPDF
from cs50 import SQL

db = SQL("sqlite:///manager.db")


class generate_pdf_report():
    def __init__(self, lable, orientation=2, font_size=2, paper_size=1):
        self.orientation = orientation
        self.font_size = font_size
        self.paper_size = paper_size
        if len(lable) == 0:
            lable = "User-System:Request[200]"
        self.lable = lable
    
    def __str__(self):
        return f"{self.orientation}, {self.font_size}, {self.lable}, {self.paper_size}"

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
    @property
    def paper_size(self):
        return self._paper_size
    
    @paper_size.setter
    def paper_size(self, size):
        print(size)
        match size:
            case 1:
                self._paper_size = "A3"
            case 2:
                self._paper_size = "A4"
            case _:
                self._paper_size = "A3"
    
    def budget_report(self, id):
        """REPORT GENERATING FUNCTION FOR BOTH LANDSCAPE AND PORTRAIT PAGES
        Arguments:
            id=:project_id in manager.db , events table
        """
        details = db.execute("SELECT * FROM events WHERE id=?", id)
        income = sorted(db.execute("SELECT * FROM budget_income WHERE project_id=?",id), key=lambda x : x["date"])
        expends = sorted(db.execute("SELECT * FROM budget_expenditure WHERE project_id=?",id), key=lambda x : x["date"]) 

        pdf = FPDF(orientation=self.orientation, format=self.paper_size)
        pdf.set_font_size(self.font_size)
        pdf.add_page()
        if self.orientation == "landscape":
            html = f"""
                    <div><h1>{details[0]["name"]}</h1><div>
                    <p>{ details[0]["description"] }</p>
                    <p>From {details[0]["starting_date"]} To {details[0]["ending_date"]}</p>
                    <p>{self.lable}</p>
                    """
            html += f"""
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
            total_income = 0
            total_expends = 0

            for _ in range(length):
                line=""
                try:
                    row1 = income[_]
                    total_amount = (float(row1['units'])*float(row1['amount']))
                    line += f"""<tr style="text-align:right;">
                                <td>{row1['date']}</td>
                                <td>{row1['type']}</td>
                                <td>{row1['item']}</td>
                                <td>{row1['units']}</td>
                                <td>{"{:.2f}".format(row1['amount'])}</td>
                                <td>{"{:.2f}".format(total_amount) }</td>"""
                    total_income += total_amount
                    
                    
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
                    total_amount = (float(row2['units'])*float(row2['amount'])) 
                    line += f"""
                                <td>{row2['date']}</td>
                                <td>{row2['type']}</td>
                                <td>{row2['item']}</td>
                                <td>{row2['units']}</td>
                                <td>{ "{:.2f}".format(row2['amount']) }</td>
                                <td>{ "{:.2f}".format(total_amount) }</td>
                                </tr>"""
                    total_expends += total_amount
                except:
                    line += f"""
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td></tr>"""
                html += line
            html += f"""
            <tr>
                <td colspan="5">Total</td>
                <td>{ "{:.2f}".format(total_income) }</td>
                <td colspan="5">Total</td>
                <td>{ "{:.2f}".format(total_expends) }</td>
            </tr>
            """ 
            html += """</tbody></table>"""
            balance = total_income - total_expends
            
            if balance > 0:
                html += f"""<p>Balance = +{"{:.2f}".format(balance)}</p>"""
            else:
                html += f"""<p>Balance = {"{:.2f}".format(balance)}</p>"""
            pdf.write_html(html , table_line_separators=True)
            pdf.output('report.pdf')
        elif self.orientation == "portrait":
            total_income = 0
            total_expends = 0
            html = f"""
                    <div><h1>{details[0]["name"]}</h1><div>
                    <p>{ details[0]["description"] }</p>
                    <p>From {details[0]["starting_date"]} To {details[0]["ending_date"]}</p>
                    <p>{self.lable}</p>
                    """
            html += f"""
                        <table border="1" style=" border-collapse: collapse; text-align:center;" ><thead>
                        <tr>
                            <th width="14%">Date</th>
                            <th width="14%">Catagory</th>
                            <th width="34%">Description [INCOME]</th>
                            <th width="6%">Units</th>
                            <th width="12%">Unit Price</th>
                            <th width="20%">Amount</th>
                        </tr></thead>
                        <tbody>
                        """
                        
            for row in income:
                total_amount = (float(row['units'])*float(row['amount']))
                html += f"""<tr style="word-wrap: break-word;">
                            <td>{row['date']}</td>
                            <td>{row['type']}</td>
                            <td>{row['item']}</td>
                            <td>{row['units']}</td>
                            <td>{"{:.2f}".format(row['amount'])}</td>
                            <td>{"{:.2f}".format(total_amount) }</td></tr>"""                        
                total_income += total_amount
            
            html += f"""
            <tr>
                <td colspan="5"><b>Total</b></td>
                <td><b>{ "{:.2f}".format(total_income) }</b></td>
            </tr>"""        
            html += """</tbody></table> <br><br>"""
            
            html += f"""
                        <table border="1" style=" border-collapse: collapse; text-align:center;" ><thead>
                        <tr>
                            <th width="14%">Date</th>
                            <th width="14%">Catagory</th>
                            <th width="34%">Description [Expends]</th>
                            <th width="6%">Units</th>
                            <th width="12%">Unit Price</th>
                            <th width="20%">Amount</th>
                        </tr></thead>
                        <tbody>
                        """
                        
            for row in expends:
                total_amount = (float(row['units'])*float(row['amount']))
                html += f"""<tr>
                            <td>{row['date']}</td>
                            <td>{row['type']}</td>
                            <td>{row['item']}</td>
                            <td>{row['units']}</td>
                            <td>{"{:.2f}".format(row['amount'])}</td>
                            <td>{"{:.2f}".format(total_amount) }</td></tr>"""                        
                total_expends += total_amount
            
            html += f"""
            <tr>
                <td colspan="5"><b>Total</b></td>
                <td><b>{ "{:.2f}".format(total_expends) }</b></td>
            </tr>"""        
            html += """</tbody></table><br><br>"""
            balance = total_income - total_expends
            
            if balance > 0:
                html += f"""<p>Balance = +{"{:.2f}".format(balance)}</p>"""
            else:
                html += f"""<p>Balance = {"{:.2f}".format(balance)}</p>"""
                
            pdf.write_html(html , table_line_separators=True)
            pdf.output('report.pdf')
            