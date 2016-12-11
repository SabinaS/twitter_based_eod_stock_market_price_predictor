#!/usr/bin/env python
import json

def getEnglishEntries( filename ):
    ''' Method for prasing a file for English entries '''
    englishEntries = []
    with open( filename ) as jData:
        for line in jData:
            jLine = json.loads( line )
            if u'user' in jLine:
                if jLine[ u'user' ][ u'lang' ] == 'en':
                    englishEntries.append( jLine )
            else:
                continue
    jData.close()
    return englishEntries

def getRelevantEntries( companyName, listOfEntries ):
    ''' Method that reads in a company name and a pre-filtered list of 
        dicts and further filters the list to only include dicts
        that have the company name in the text '''
    relevantEntries = []
    for entry in listOfEntries:
        if u'text' in entry and u'entities' in entry:
            if companyName in entry[ u'text' ] or companyName in entry[ u'entities' ]:
                relevantEntries.append( entry )
            else:
                continue
        else:
            continue
    return relevantEntries

def writeOutputJSON( companyName, listOfEntries) :
    ''' Method for taking in a list of entries and writing an output json
        file containing those entries '''
    strListOfEntries = [ str( entry ) for entry in listOfEntries ]
    with open( companyName+'.json', 'a+' ) as en:
        en.write( '\n'.join( strListOfEntries ) )
    en.close()

if __name__ == "__main__":
    import sys
    englishEntries = getEnglishEntries( sys.argv[ 1 ] )
    relevantEntries = getRelevantEntries( sys.argv[ 2 ], englishEntries )
    writeOutputJSON( sys.argv[ 2 ], relevantEntries )
