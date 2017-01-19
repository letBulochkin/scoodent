"""GUI widgets."""

from datetime import date, datetime

from PyQt4 import uic
from PyQt4.QtCore import QDate
from PyQt4.QtGui import (
    QDialog, QItemSelectionModel, QLineEdit, QMainWindow,
    QMessageBox, QPushButton, QTableWidgetItem, QVBoxLayout
)

from scoodent.common import db, config
from scoodent.models import Actor, Genre, Disk, Customer, Rental


def from_date(date):
    """Return QDate object from datetime.date."""

    return QDate(date.year, date.month, date.day)


def to_date(qdate):
    """Return datetime.date object from QDate."""

    return date(day=qdate.day(), month=qdate.month(), year=qdate.year())


def from_datetime(datetime):

    return QDateTime(datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute)


def to_datetime(qdatetime):

    return datetime(minute=qdatetime.minute(), hour=qdatetime.hour(), day=qdatetime.day(), month=qdatetime.month(), year=qdatetime.year())

class DeleteDialog(QDialog):
    """Represents dialog for delete confirmation."""

    def __init__(self, what, from_what):
        QDialog.__init__(self)
        self.msg = "Delete {w} from {f} table?".format(w=what, f=from_what)
        uic.loadUi(config.UI["delete_dialog"], self)
        self.label.setText(self.msg)


def required_field_empty_warning(parent, msg="One or more fields are empty."):
    """Warn user."""

    QMessageBox.warning(parent, "Error", msg)

class DiskDialog(QDialog):

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["disk_dialog"], self)

        self.disk_id = model_id
        self.pb_add_disk.clicked.connect(self.add_disk)

        self.load_disk_info()

    def load_disk_info(self):

        session = db.get_session()
        disk = session.query(Disk).filter(
            Disk.id == self.disk_id
        ).first()

        self.le_title.setText(disk.title)
        self.le_director.setText(disk.director)
        self.le_year.setText(str(disk.year))
        self.cd_existance.setChecked(disk.existance)
        self.de_acq_date.setDate(from_date(disk.acq_date))
        self.sb_rating.setValue(disk.rating)

    def add_disk(self):

        disk = {
            "acq_date": to_date(self.de_acq_date.date()),
            "title": str(self.le_title.text()),
            "director": str(self.le_director.text()),
            "year": int(self.le_year.text()),
            # "actors":
            # "genre":
            "rating": int(self.sb_rating.value()),
            "existance": self.cd_existance.checked(),
        }

class CustomerDialog(QDialog):
    """Implements student interaction."""

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["customer_dialog"], self)

        self.customer_id = model_id
        self.pb_add_customer.clicked.connect(self.add_customer)

        self.load_customer_info()

    def load_customer_info(self):
        """Get all needed info from DB."""

        session = db.get_session()
        customer = session.query(Customer).filter(
            Customer.id == self.customer_id
        ).first()

        self.le_ph_number.setText(customer.phone_number)
        self.le_name.setText(customer.name)
        self.le_passport.setText(customer.passport)
        self.le_ordered.setText(str(customer.ordered))
        '''
        self.le_parents_phone.setText(student.parents_phone)
        self.le_school.setText(student.school)
        self.de_enter_date.setDate(from_datetime(student.enter_date))
        '''

    def add_customer(self):
        # from datetime import datetime
        # datetime.now()
        customer = {
            "phone_number": str(self.le_ph_number.text()),
            "name": str(self.le_name.text()),
            "passport": str(self.le_passport.text()),
            "ordered": int(self.le_ordered.text()),
        }

        if not all(customer.values()):
            required_field_empty_warning(self)
        else:
            db.insert_objects(Student(**student))


class RentalDialog(QDialog):
    """Implements reports interaction."""

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["rental_dialog"], self)

        self.rental_id = model_id
        self.pb_add_rental.clicked.connect(self.add_rental)

        self.load_rental_info()

    def load_rental_info(self):
        """Get all needed info from DB."""

        session = db.get_session()
        rental = session.query(Rental).filter(
            Rental.id == self.rental_id
        ).first()

        self.le_customer.setText(str(rental.rent_customer))
        self.customer_name = rental.customer.name
        self.le_disk.setText(str(rental.rent_customer))
        self.disk_title = rental.disk.title
        self.cd_returned.setChecked(rental.returned)
        self.dte_time_taken.setDateTime(from_datetime(rental.time_taken))
        # self.dte_time_returned.setDateTime(from_datetime(rental.time_returned))
        self.le_deposit.setText(rental.deposit)

    def add_rental(self):
        """Add report to DB."""
        #TODO

        session = db.get_session()
        rental = {
            # "rent_customer": str(self.le_rent_customer()),
            # "rent_disk": str(self.le_rent_disk()),
            "rent_customer": session.query(Customer).filter(
                Customer.id == int(self.le_customer.text())),
            "rent_disk": session.query(Disk).filter(
                Disk.id == int(self.le_disk.text())),
            "returned": self.cd_returned.checked(),
            "time_taken": to_datetime(self.dte_time_taken.datetime()),
            # "time_returned"
            "deposit": int(self.le_deposit.text()),
        }

        if not all(report.values()):
            required_field_empty_warning(self)
        else:
            db.insert_objects(Report(**report))


class GenreDialog(QDialog):

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["genre_dialog"], self)

        self.genre_id = model_id
        self.pb_add_genre.clicked.connect(self.add_genre)

        self.load_genre_info()

    def load_genre_info(self):
        session = db.get_session()
        genre = session.query(Genre).filter(
            Genre.id == self.genre_id
        ).first()

        self.le_name.setText(genre.film_genre if genre else "")

    def add_genre(self):
        """Insert new genre to DB."""

        name = str(self.le_name.text())
        if not name:
            required_field_empty_warning(self)
        else:
            db.insert_objects(Genre(film_genre=name))


class ActorDialog(QDialog):

    def __init__(self, model_id):
        QDialog.__init__(self)
        uic.loadUi(config.UI["actor_dialog"], self)

        self.actor_id = model_id
        self.pb_add_actor.clicked.connect(self.add_actor)

        self.load_actor_info()

    def load_actor_info(self):
        session = db.get_session()
        actor = session.query(Actor).filter(
            Actor.id == self.actor_id
        ).first()

        self.le_name.setText(actor.name if actor else "")

    def add_actor(self):
        """Insert new actor to DB."""

        name = str(self.le_name.text())
        if not name:
            required_field_empty_warning(self)
        else:
            db.insert_objects(Actor(name=name))


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(config.UI["main"], self)

        self.selected = None
        self.model = Disk

        self.dialog_by_model = {
            Actor: ActorDialog,
            Genre: GenreDialog,
            Disk: DiskDialog,
            Customer: CustomerDialog,
            Rental: RentalDialog,
        }

        self.action_exit.triggered.connect(self.close)

        # TODO
        def pb_add_callback():
            """Call dialog for current model."""
            
            self.dialog_by_model[self.model](1).exec_()
            self.show_table(self.model)

        self.pb_add.clicked.connect(pb_add_callback)
        self.pb_delete.clicked.connect(self.remove_selected)

        self.rb_actor.clicked.connect(lambda: self.show_table(Actor))
        self.rb_genre.clicked.connect(lambda: self.show_table(Genre))
        self.rb_disk.clicked.connect(lambda: self.show_table(Disk))
        self.rb_customer.clicked.connect(lambda: self.show_table(Customer))
        self.rb_rental.clicked.connect(lambda: self.show_table(Rental))

        # TODO
        self.table_widget.cellClicked.connect(self.select_table_row)
        self.table_widget.cellDoubleClicked.connect(self.open_table_info)
        # TODO: get current selection or QMessageBox.error/ignore
        # self.pb_view_and_modify.clicked.connect(self.table_widget.cellDoubleClicked)  # self.open_table_info)

        self.show_table(self.model)

    def show_table(self, model):
        """Show all entries of model in table."""

        self.model = model
        session = db.get_session()
        names = model.__table__.columns.keys()
        data = list(session.query(model))

        rows = len(data)
        cols = len(names)
        self.table_widget.clear()
        self.table_widget.setSortingEnabled(True)
        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(cols)
        self.table_widget.setHorizontalHeaderLabels(names)
        # self.table_widget.sortByColumn(0, Qt.AscendingOrder)

        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem(str(data[row].__dict__[names[col]]))
                self.table_widget.setItem(row, col, item)

    def select_table_row(self, row, column):
        """Select current table row."""

        self.selected = (row, column)
        # self.table_widget.setCurrentIndex(
        #     (row, column), QItemSelectionModel.NoUpdate)

    def remove_selected(self):
        """Remove selected item from current table."""

        if not self.selected:
            required_field_empty_warning(self, "Select item for removal.")

        # on (row, 0) placed entity ID
        model_id = int(self.table_widget.item(self.selected[0], 0).text())

        if not DeleteDialog(
                "item with ID = {0}".format(model_id), self.model.__tablename__
        ).exec_() == QDialog.Accepted:
            return

        session = db.get_session()
        session.query(self.model).filter(self.model.id == model_id).delete()
        session.commit()
        self.show_table(self.model)

    def open_table_info(self, row, column):
        """Open current table info window."""

        dialog = self.dialog_by_model.get(self.model)
        model_id = int(self.table_widget.item(row, 0).text())
        dialog(model_id=model_id).exec_()


class LoginWindow(QDialog):
    """Login dialog window."""

    def __init__(self):
        QDialog.__init__(self)
        self.login = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.b_login = QPushButton("Login", self)
        self.b_login.clicked.connect(self.handle_login)
        layout = QVBoxLayout(self)
        layout.addWidget(self.login)
        layout.addWidget(self.password)
        layout.addWidget(self.b_login)

    def handle_login(self):
        """Login handler."""

        # TODO: get user from database
        if (
                self.login.text() == "admin" and
                self.password.text() == "admin"
        ):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Bad user or password")

    @staticmethod
    def do_login():
        return LoginWindow().exec_() == QDialog.Accepted
