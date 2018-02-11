import argparse
import datetime
from running_percentile import RunningPercentile


def string_to_date(date_string):
    """Convert date information in string to date structure, return None if it is invalid."""
    try:
        dt = datetime.datetime.strptime(date_string, "%m%d%Y")
        return dt.date()
    except:
        return None


class RecipientZipYear:
    """Identifier for each recipient in every zip code each year.
    To be used as keys in dictionary, hash function and comparator are provided.
    """

    def __init__(self, recipient, zip_code, year):
        self.recipient = recipient
        self.zip_code = zip_code
        self.year = year

    def __eq__(self, other):
        if not isinstance(other, RecipientZipYear):
            return False
        else:
            return self.recipient == other.recipient and self.zip_code == other.zip_code and self.year == other.year

    def __ne__(self, other):
        if not isinstance(other, RecipientZipYear):
            return True
        else:
            return self.recipient != other.recipient or self.zip_code != other.zip_code or self.year != other.year

    def __hash__(self):
        return hash(self.recipient) + hash(self.zip_code) + hash(self.year)

    def __str__(self):
        return '(' + self.recipient + ', ' + self.zip_code + ',' + str(self.year) + ')'


class Donor:
    """Combination of name and zip code for a certain donor.
    To be used as keys in dictionary, hash function and comparator are provided.
    """

    def __init__(self, name, zip_code):
        self.name = name.upper()
        self.zip_code = zip_code

    def __eq__(self, other):
        if not isinstance(other, Donor):
            return False
        else:
            return self.name == other.name and self.zip_code == other.zip_code

    def __ne__(self, other):
        if not isinstance(other, Donor):
            return True
        else:
            return self.name != other.name or self.zip_code != other.zip_code

    def __hash__(self):
        return hash(self.name) + hash(self.zip_code)

    def __str__(self):
        return '(' + self.name + ', ' + self.zip_code + ')'


class DonationAnalytics:
    """Main class for donation analytics, recording target percentile, each donor information.
    Take each record line as input.
    """

    def __init__(self, percentile):
        self.percentile = percentile
        self.repeat = dict()              # key: Donor, value: {year}
        self.running_percentile = dict()  # key: RecipientZipYear, value: RunningPercentile

    def repeat_donor(self, name, zip_code, year):
        """Find whether a certain donor is a repeat donor in any prior year.
        No matter yes or no, mark this donor as contributed.
        """
        donor = Donor(name, zip_code)
        if donor in self.repeat:
            self.repeat[donor].add(year)
            for y in self.repeat[donor]:
                if y < year:
                    return True
            return False
        else:
            self.repeat[donor] = {year}
            return False

    def print_record(self, key):
        """Output one result record."""
        percentile_amount = str(self.running_percentile[key].get_percentile())
        total_amount = str(round(self.running_percentile[key].total_amount))
        count = str(len(self.running_percentile[key]))
        record = [key.recipient, key.zip_code, str(key.year), percentile_amount, total_amount, count]
        return '|'.join(record)

    def process_line(self, line):
        """Process one line from input file. Check whether this line is malformed, and ignore malformed line.
        Return None if this line is ignored, otherwise return corresponding output line.
        """
        if len(line) == 0:
            return None

        columns = line.split('|')
        cmte_id, name, zip_code = columns[0], columns[7], columns[10][:5]
        transaction_dt, transaction_amt = columns[13], columns[14]
        other_id = columns[15]

        if len(other_id) > 0 or len(transaction_amt) == 0 or len(cmte_id) == 0 or len(zip_code) < 5:
            return None            # malformed data fields, ignore this line
        transaction_date = string_to_date(transaction_dt)
        if transaction_date is None:
            return None            # 'TRANSACTION_DT' is an invalid date

        if self.repeat_donor(name, zip_code, transaction_date.year):
            # this record is from a repeat donor in any prior calendar year
            amount = float(transaction_amt)
            key = RecipientZipYear(cmte_id, zip_code, transaction_date.year)
            if key not in self.running_percentile:
                self.running_percentile[key] = RunningPercentile(self.percentile)
            self.running_percentile[key].add(amount)
            return self.print_record(key)
        else:
            return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_cont', help='Contribution input file name')
    parser.add_argument('input_percentile', help='Percentile input file name')
    parser.add_argument('output', help='Output file name')
    args = parser.parse_args()

    file_percentile = open(args.input_percentile)
    percentile = int(file_percentile.readline().strip())
    file_percentile.close()

    analyzer = DonationAnalytics(percentile/100.0)

    file_output = open(args.output, 'w')
    file_cont = open(args.input_cont)

    for line in file_cont:
        record = analyzer.process_line(line.strip())
        if record is not None:
            file_output.write(record + '\n')

    file_cont.close()
    file_output.close()


if __name__ == '__main__':
    main()
