from collections import defaultdict
from odoo import fields, models
import requests
import logging

_logger = logging.getLogger(__name__)

class ResCurrencyRateProviderDolarAPI(models.Model):
    _inherit = "res.currency.rate.provider"

    service = fields.Selection(
        selection_add=[("DOLARAPI", "DolarAPI")],
        ondelete={"DOLARAPI": "set default"},
    )

    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service != "DOLARAPI":
            return super()._get_supported_currencies()

        # En este caso, solo soportamos USD.
        return ["USD"]

    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        self.ensure_one()
        if self.service != "DOLARAPI":
            return super()._obtain_rates(
                base_currency, currencies, date_from, date_to
            )

        url = "https://dolarapi.com/v1/dolares/oficial"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Obtener tasa de compra y fecha de actualización
            usd_to_ars_rate = data["compra"]
            rate_date = fields.Date.from_string(data["fechaActualizacion"])

            content = defaultdict(dict)
            if rate_date >= date_from and rate_date <= date_to:
                for currency in currencies:
                    if base_currency == "ARS" and currency == "USD":
                        # Invertir tasa porque el API devuelve ARS por USD
                        content[rate_date.isoformat()]["USD"] = str(1 / usd_to_ars_rate)
                    elif base_currency == "USD" and currency == "ARS":
                        # Usar tasa directa del API
                        content[rate_date.isoformat()]["ARS"] = str(usd_to_ars_rate)
                    else:
                        # Error: Solo se soporta conversión entre USD y ARS
                        _logger.warning(
                            "Conversión no soportada: Base=%s, Moneda=%s",
                            base_currency,
                            currency,
                        )
            return content
        except Exception as e:
            _logger.error("Error al obtener tasas desde DolarAPI: %s", e)
            return defaultdict(dict)


