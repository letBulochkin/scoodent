"""GUI widgets."""

from datetime import date, datetime

from PyQt4 import uic
from PyQt4.QtCore import QDate, QDateTime
from PyQt4.QtGui import (
    QDialog, QItemSelectionModel, QLineEdit, QMainWindow,
    QMessageBox, QPushButton, QTableWidgetItem, QVBoxLayout, QLabel, QHeaderView
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

    if datetime is not None:
        return QDateTime(
            datetime.year, datetime.month,
            datetime.day,datetime.hour,
            datetime.minute
            )
    else:
        return QDateTime.currentDateTime()


def to_datetime(qdatetime):

    return datetime(
        minute=qdatetime.minute(),
        hour=qdatetime.hour(),
        day=qdatetime.day(),
        month=qdatetime.month(),
        year=qdatetime.year()
    )


def count_curr_deposit():
    """Count sum of all deposits available."""

    res = 0

    session = db.get_session()
    depo = session.query(Rental).filter(
        Rental.time_returned == None
    ).all()

    for i in depo:
        res += i.deposit

    return res


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


# TODO: Update list of required fields
class DiskDialog(QDialog):

    def __init__(self, model_id=None):
        QDialog.__init__(self)
        uic.loadUi(config.UI["disk_dialog"], self)

        self.disk_id = model_id
        self.pb_add_disk.clicked.connect(self.add_disk)

        if model_id is not None:
            self.load_disk_info()

    def load_disk_info(self):

        session = db.get_session()
        disk = session.query(Disk).filter(
            Disk.id == self.disk_id
        ).first()

        genre = [
            str(gen.film_genre) for gen in disk.genre]

        actors = [
            act.name for act in disk.actors]

        self.le_title.setText(disk.title)
        self.le_director.setText(disk.director)
        self.le_year.setText(str(disk.year))
        self.le_genre.setText(", ".join(genre))
        self.le_actors.setText(", ".join(actors))
        self.cb_existance.setChecked(disk.existance)
        self.de_acq_date.setDate(from_date(disk.acq_date))
        self.sb_rating.setValue(disk.rating)

    def add_disk(self):

        session = db.get_session()

        actors = [
            resp
            for name in map(str.strip, str(self.le_actors.text()).split(","))
            for resp in session.query(Actor).filter(Actor.name == name)]

        genre = [
            resp
            for name in map(str.strip, str(self.le_genre.text()).split(","))
            for resp in session.query(Genre).filter(Genre.film_genre == name)]

        disk = {
            "acq_date": to_date(self.de_acq_date.date()),
            "title": str(self.le_title.text()),
            "director": str(self.le_director.text()),
            "year": int(self.le_year.text()),
            "rating": int(self.sb_rating.value()),
            "existance": self.cb_existance.isChecked(),
            "actors": actors,
            "genre": genre
        }

        disk = Disk(**disk)

        # if not all(disk.values()):
        #     required_field_empty_warning(self)
        # else:

        db.insert_objects(disk, self.disk_id)


class CustomerDialog(QDialog):
    """Implements student interaction."""

    def __init__(self, model_id=None):
        QDialog.__init__(self)
        uic.loadUi(config.UI["customer_dialog"], self)

        self.customer_id = model_id
        self.pb_add_customer.clicked.connect(self.add_customer)

        if model_id is not None:
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

        # self.le_parents_phone.setText(student.parents_phone)
        # self.le_school.setText(student.school)
        # self.de_enter_date.setDate(from_datetime(student.enter_date))

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
            db.insert_objects(Customer(**customer), self.customer_id)


class RentalDialog(QDialog):
    """Implements rentals interaction."""

    def __init__(self, model_id=None):
        QDialog.__init__(self)
        uic.loadUi(config.UI["rental_dialog"], self)

        self.upd = False

        self.rental_id = model_id
        self.pb_add_rental.clicked.connect(self.add_rental)

        def switch():
            self.dte_time_returned.setEnabled(True)
            self.upd = True

        # TODO: Rewrite this
        if model_id is not None:
            self.load_rental_info()
            if self.cb_returned.isChecked():
                self.dte_time_returned.setEnabled(True)
            elif not self.cb_returned.isChecked():
                self.cb_returned.stateChanged.connect(lambda: switch())

    def load_rental_info(self):
        """Get all needed info from DB."""

        self.cb_returned.setEnabled(True)

        session = db.get_session()
        rental = session.query(Rental).filter(
            Rental.id == self.rental_id
        ).first()

        # TODO: Disk return time
        self.le_customer.setText(str(rental.rent_customer))
        self.customer_name.setText(
            session.query(Customer).filter(
                Customer.id == rental.rent_customer
            ).first().name
        )
        self.le_disk.setText(str(rental.rent_disk))
        self.disk_title.setText(
            session.query(Disk).filter(
                Disk.id == rental.rent_disk
            ).first().title
        )
        self.dte_time_taken.setDateTime(from_datetime(rental.time_taken))
        self.dte_time_returned.setDateTime(from_datetime(rental.time_returned))
        self.le_deposit.setText(str(rental.deposit))

    def add_rental(self):
        """Add rental to DB."""

        # TODO: Check whether disk is available
        session = db.get_session()
        rental = {
            "rent_customer": int(self.le_customer.text()),
            "rent_disk": int(self.le_disk.text()),
            "returned": False,
            "time_taken": self.dte_time_taken.dateTime().toPyDateTime(),
            "time_returned": None,
            "deposit": int(self.le_deposit.text()),
        }

        if self.upd:
            rental["returned"] = True
            rental["time_returned"] = self.dte_time_returned.dateTime().toPyDateTime()

        # TODO: Do smth with disk return time
        # if not all(rental.values()):
        #    required_field_empty_warning(self)
        # else:

        db.insert_objects(Rental(**rental), self.rental_id)

        # TODO: implement this via ORM trigger, not user interface
        r_disk = session.query(Disk).filter(Disk.id == rental["rent_disk"]).first()
        r_disk.existance = self.upd
        db.insert_objects(r_disk, r_disk.id)


class GenreDialog(QDialog):
    """Implements Genre interaction."""

    def __init__(self, model_id=None):
        QDialog.__init__(self)
        uic.loadUi(config.UI["genre_dialog"], self)

        self.genre_id = model_id
        self.pb_add_genre.clicked.connect(self.add_genre)

        if model_id is not None:
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
            db.insert_objects(Genre(film_genre=name), self.genre_id)


class ActorDialog(QDialog):
    """Implements Actor interaction."""

    def __init__(self, model_id=None):
        QDialog.__init__(self)
        uic.loadUi(config.UI["actor_dialog"], self)

        self.actor_id = model_id
        self.pb_add_actor.clicked.connect(self.add_actor)

        if model_id is not None:
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
            db.insert_objects(Actor(name=name), self.actor_id)


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

            self.dialog_by_model[self.model]().exec_()
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
        self.table_widget.horizontalHeader().setResizeMode(QHeaderView.Fixed)
        # self.table_widget.sortByColumn(0, Qt.AscendingOrder)

        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem(str(data[row].__dict__[names[col]]))
                self.table_widget.setItem(row, col, item)

        self.l_curr_deposit.setText(str(count_curr_deposit()))

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
        rm_model = session.query(self.model).filter(self.model.id == model_id).first()
        session.delete(rm_model)
        session.commit()
        self.show_table(self.model)

    def open_table_info(self, row, column):
        """Open current table info window."""

        dialog = self.dialog_by_model.get(self.model)
        model_id = int(self.table_widget.item(row, 0).text())
        dialog(model_id=model_id).exec_()
        self.show_table(self.model)


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
