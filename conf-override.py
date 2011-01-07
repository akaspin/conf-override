'''
Created on 06.01.2011

@author: spin
'''

import glob
import sys
import optparse

class Processor:
    def __init__(self, base, marker):
        self.baselines = open(base, 'r').read().split('\n')
        self.marker = marker
        self.ops = []
        self.sources = []
        self.out = []
        
    def go(self):
        for line in self.baselines:
            (dir, data) = self.extract_directive(line)
            
            if dir == 'gather':
                self.add_sources(data)
            else:
                self.ops.append((dir, data))
            
        self.extract_sources_blocks()
        self.finish()        

    def finish(self):
        for op in self.ops:
            if op[0] == 'raw':
                self.out.append(op[1])
            elif op[0] == 'block' and self.blocks[op[1]]:
                for line in self.blocks[op[1]]:
                    self.out.append(line)
                
        print '\n'.join(self.out)

    def extract_sources_blocks(self):
        self.sources = list(set(self.sources))
        self.blocks = {}
        for source in self.sources:
            block = None
            for line in open(source, 'r').read().split('\n'):
                (dir, data) = self.extract_directive(line)
                
                if dir == 'block':
                    block = data
                    self.blocks[block] = []
                elif block:
                    self.blocks[block].append(line)
                
    def add_sources(self, line):
        for patt in line.split(' '):
            for file in glob.glob(patt):
                self.sources.append(file)
            
    def extract_directive(self, line):
        stripped = line.strip()
        if stripped.startswith(self.marker):
            # May be directive
            candidate = stripped[len(self.marker):].strip()
            if candidate.startswith('+++'):
                # Gather
                return ('gather', candidate[3:].strip())
            elif candidate.startswith('<<<'):
                # Block
                return ('block', candidate[3:].strip())
            else:
                # Raw
                return ('raw', line)
        else:
            # Just raw
            return ('raw', line)

if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [options] base')
    parser.add_option('-m', '--marker', action='store', dest='marker',
                      type='string', default='#', help='Override marker')
    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        parser.error("Provide base filename")
    
    proc = Processor(args[0], options.marker)
    proc.go()
