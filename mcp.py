import mcp3008

while True:
    with mcp3008.MCP3008() as adc:
        # print(type(adc.read([mcp3008.CH7]))) # prints raw data [CH0]
        chan = adc.read([mcp3008.CH7])
        print(chan[0])
