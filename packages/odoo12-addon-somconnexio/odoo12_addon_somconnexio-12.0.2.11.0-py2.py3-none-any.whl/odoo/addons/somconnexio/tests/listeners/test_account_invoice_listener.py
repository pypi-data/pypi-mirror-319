from mock import patch
from odoo.addons.component.tests.common import ComponentMixin
from odoo.tests.common import SavepointCase


@patch("odoo.addons.somconnexio.listeners.account_invoice_listener.NotifyInvoiceNumber")
class TestAccountInvoiceListener(SavepointCase, ComponentMixin):
    @classmethod
    def setUpClass(cls):
        super(TestAccountInvoiceListener, cls).setUpClass()
        cls.setUpComponent()

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        SavepointCase.setUp(self)
        ComponentMixin.setUp(self)

        self.partner = self.env.ref("somconnexio.res_partner_2_demo")

    def test_update_invoice_number_notify_BI_API(self, NotifyInvoiceNumberMock):
        self.product = self.browse_ref("somconnexio.Fibra100Mb")
        self.price_unit = 41
        self.quantity = 1
        self.account = self.env["account.account"].search([("code", "=", "43000000")])
        tax_id = (
            self.env["account.tax"].search([("name", "=", "IVA 21% (Servicios)")]).id
        )
        invoice_line_params = {
            "name": self.product.name,
            "product_id": self.product.id,
            "quantity": self.quantity,
            "price_unit": self.price_unit,
            "account_id": self.account.id,
            "invoice_line_tax_ids": [(4, tax_id, 0)],
        }
        invoice_line = self.env["account.invoice.line"].create(invoice_line_params)
        invoice_params = {
            "partner_id": self.partner.id,
            "date_invoice": "2023-11-01",
            "invoice_line_ids": [(6, 0, [invoice_line.id])],
        }
        invoice = self.env["account.invoice"].create(invoice_params)
        invoice.action_invoice_open()

        self.assertTrue(invoice.number)

        NotifyInvoiceNumberMock.assert_called_once_with(invoice.number)
        NotifyInvoiceNumberMock.return_value.run.assert_called_once()
