import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor
from esphome.const import CONF_ID, \
    CONF_BATTERY_LEVEL, CONF_BATTERY_VOLTAGE, CONF_BRIGHTNESS, \
    DEVICE_CLASS_VOLTAGE, STATE_CLASS_MEASUREMENT, \
    UNIT_PERCENT, UNIT_VOLT, ICON_BATTERY, ICON_FLASH

DEPENDENCIES = ['i2c']

CONF_VBUS_VOLTAGE = 'vbus_voltage'

axp192_ns = cg.esphome_ns.namespace('axp192')

AXP192Component = axp192_ns.class_('AXP192Component', cg.PollingComponent, i2c.I2CDevice)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(AXP192Component),
    cv.Optional(CONF_BATTERY_LEVEL):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=1,
            icon=ICON_BATTERY,
        ),
    cv.Optional(CONF_BATTERY_VOLTAGE):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=3,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    cv.Optional(CONF_VBUS_VOLTAGE):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=3,
            icon=ICON_FLASH,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    cv.Optional(CONF_BRIGHTNESS, default=1.0): cv.percentage,
}).extend(cv.polling_component_schema('60s')).extend(i2c.i2c_device_schema(0x77))


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield i2c.register_i2c_device(var, config)

    if CONF_BATTERY_LEVEL in config:
        conf = config[CONF_BATTERY_LEVEL]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_batterylevel_sensor(sens))

    if CONF_BATTERY_VOLTAGE in config:
        conf = config[CONF_BATTERY_VOLTAGE]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_batteryvoltage_sensor(sens))

    if CONF_VBUS_VOLTAGE in config:
        conf = config[CONF_VBUS_VOLTAGE]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_vbusvoltage_sensor(sens))

    if CONF_BRIGHTNESS in config:
        conf = config[CONF_BRIGHTNESS]
        cg.add(var.set_brightness(conf))
