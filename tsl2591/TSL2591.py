#!/usr/bin/python
from Adafruit_I2C import Adafruit_I2C

class TSL2591:
  i2c = None
  
  # Channels
  __CH0				= 0 	# FULLSPECTRUM
  __CH1				= 1   # INFRARED
  __CH2				= 2 	# VISIBLE 

  # Chip
  __ADDRESS			= 0x29
  __READBIT			= 0x01

  # Command
  __COMMAND_BIT			= 0xA0 	# bits 7 and 5 for 'command normal'
  __CLEAR_BIT			  = 0x40 	# Clears any pending interrupt (write 1 to clear)
  __WORD_BIT			  = 0x20  # 1 = read/write word (rather than byte)
  __BLOCK_BIT 			= 0x10	# 1 = using block read/write

  __ENABLE_POWERON    		= 0x01
  __ENABLE_POWEROFF   		= 0x00
  __ENABLE_AEN        		= 0x02
  __ENABLE_AIEN       		= 0x10

  __CONTROL_RESET     		= 0x80

  # Lux
  __LUX_DF            		= 408.0
  __LUX_COEFB         		= 1.64	# CH0 coefficient 
  __LUX_COEFC         		= 0.59 	# CH1 coefficient A
  __LUX_COEFD         		= 0.86 	# CH2 coefficient B

  # Registers
  __REG_ENABLE           	= 0x00
  __REG_CONTROL          	= 0x01
  __REG_THRESHHOLDL_LOW  	= 0x02
  __REG_THRESHHOLDL_HIGH 	= 0x03
  __REG_THRESHHOLDH_LOW  	= 0x04
  __REG_THRESHHOLDH_HIGH 	= 0x05
  __REG_INTERRUPT        	= 0x06
  __REG_CRC              	= 0x08
  __REG_PACKAGE		 	      = 0x11
  __REG_ID			          = 0x12
  __REG_STATUS		 	      = 0x13
  __REG_CHAN0_LOW        	= 0x14
  __REG_CHAN0_HIGH       	= 0x15
  __REG_CHAN1_LOW        	= 0x16
  __REG_CHAN1_HIGH       	= 0x17

  # Integration
  __INTEGRATIONTIME_100MS     	= 0x00
  __INTEGRATIONTIME_200MS     	= 0x01
  __INTEGRATIONTIME_300MS     	= 0x02
  __INTEGRATIONTIME_400MS     	= 0x03
  __INTEGRATIONTIME_500MS     	= 0x04
  __INTEGRATIONTIME_600MS     	= 0x05

  # Gain
  __GAIN_LOW         		  = 0x00    # low gain (1x)
  __GAIN_MED            	= 0x10    # medium gain (25x)
  __GAIN_HIGH           	= 0x20    # medium gain (428x)
  __GAIN_MAX            	= 0x30    # max gain (9876x)

  def __init__(self, address=__ADDRESS, debug=False):
    self.i2c = Adafruit_I2C(address, debug=debug)
    self.address = address
    self.debug = debug

    self._initialized = False
    self._integration = self.__INTEGRATIONTIME_100MS
    self._gain        = self.__GAIN_MED

  def begin(self):
    id = self.readID()
    if (id != 0x50):
      return False
    self._initialized = True
    
    if (self.debug):
      print '[begin] _initialized = ', self._initialized 

    self.setTiming(self._integration)
    self.setGain(self._gain)
    self.disable()
    return True

  def initAndBegin(self):
    if (self._initialized):
      return True
    else:
      return self.begin()
  
  def enable(self, aen=False, aien=False):
    initSuccess = self.initAndBegin()
    if (not initSuccess):
      return

    print '[enable]'
    self.i2c.write8(self.__COMMAND_BIT | self.__REG_ENABLE, 
        self.__ENABLE_POWERON | (aen & self.__ENABLE_AEN) | (aien & self.__ENABLE_AIEN))

  def disable(self):
    initSuccess = self.initAndBegin()
    if (not initSuccess):
      return

    print '[disable]'
    self.i2c.write8(self.__COMMAND_BIT | self.__REG_ENABLE, 
        self.__ENABLE_POWEROFF)

  def setGain(self, gain):
    initSuccess = self.initAndBegin()
    if (not initSuccess):
      return

    self._gain = gain
    print '[setGain]'
    self.i2c.write8(self.__COMMAND_BIT | self.__REG_CONTROL, self._integration | self._gain)
    self.disable()

  def getGain(self):
    return self._gain

  def setTiming(self, integration):
    initSuccess = self.initAndBegin()
    if (not initSuccess):
      return

    self._integration = integration
    print '[setTiming]'
    self.i2c.write8(self.__COMMAND_BIT | self.__REG_CONTROL, self._integration | self._gain)
    self.disable()

  def getTiming(self):
    return self._integration

  def read8(self, reg):
    return self.i2c.readU8(self.__COMMAND_BIT | reg)

  def read16(self, reg):
    return self.i2c.readU16(self.__COMMAND_BIT | reg)

  def readPackage(self):
    print '[readPackage]'
    return self.read8(self.__REG_PACKAGE)

  def readID(self):
    print '[readID]'
    return self.read8(self.__REG_ID)

  def readStatus(self):
    print '[readStatus]'
    return self.read8(self.__REG_STATUS)

  def getIntegrationTime(integration):
    atime = {
      self.__INTEGRATIONTIME_100MS: 100.0,
      self.__INTEGRATIONTIME_200MS: 200.0,
      self.__INTEGRATIONTIME_300MS: 300.0,
      self.__INTEGRATIONTIME_400MS: 400.0,
      self.__INTEGRATIONTIME_500MS: 500.0,
      self.__INTEGRATIONTIME_600MS: 600.0,
    }
    return atime[integration]()

  def getAmplifiersValue(gain):
    again = {
      self.__GAIN_LOW:  1.0,
      self.__GAIN_MED:  25.0,
      self.__GAIN_HIGH: 428.0,
      self.__GAIN_MAX:  9876.0
    }
    return again[gain]()

  def getFullLuminosity(self):
    initSuccess = self.initAndBegin()
    if (not initSuccess):
      return

    self.enable()
    for x in range(0, self._integration):
      sleep(0.12)

    print '[getFullLuminosity] ch0'
    ch0 = self.read16(self.__REG_CHAN0_LOW)
    print '[getFullLuminosity] ch1'
    ch1 = self.read16(self.__REG_CHAN1_LOW)
    if (self.debug):
      print '[getFullLuminosity] ch0 = ', hex(ch0) 
      print '[getFullLuminosity] ch1 = ', hex(ch1) 

    self.disable()
    return (ch1 << 16) | ch0
