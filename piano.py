import midi
import sys
import pickle
import pygame
import pygame.midi
import time
import operator
from Tkinter import *
import threading
import math

class Piano(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)    
        self.parent = parent  
        self.initUI()  
        
    def initUI(self):
        global canvas
        canvas = Canvas(self)
        self.parent.title("Piano")        
        self.pack(fill=BOTH, expand=1)
        self.CreateKeys()
        canvas.pack(fill=BOTH, expand=1)

    def initMidi(self):
        global player
        global tickno
        global timing
        global notelist
        global midiOutput

        notelist = []
        tracks = []
        tickno = 0
        tempo = 0
        timing = 0
        midifile = "bumblebee.mid"

        #Initialize pygame module for playback
        pygame.midi.init()
        player = pygame.midi.Output(0)
        player.set_instrument(0)
        midiOutput = midi.read_midifile(midifile)
        index = -1

        i = 0
        #List all tracks in the midifile
        for track in midiOutput:
            tracks.append(track)
            i+=1
            for event in track:
                if isinstance(event, midi.TrackNameEvent):
                    index += 1
                    print str(index) + ": " + str(event.text)
                elif isinstance(event, midi.SetTempoEvent):
                    tempo = int(event.get_bpm())
                    timing = int(event.get_mpqn() / 1000.0)

        #Prompt for User Input
        if index == -1:
            print "No valid MIDI tracks found: exiting"
        else:
            print "\nChoose a Track to Play on the Virtual Keyboard!\n"
            trackno = -1
            firstattempt = 1
            while trackno < 0 or trackno > index:
                if firstattempt:
                    trackno = int(raw_input("Track Number: "))
                    firstattempt = 0
                else:
                    trackno = int(raw_input("Invalid Track, Input Track Number: "))         
            tempo = int(raw_input("File Tempo (Original = "+str(tempo)+" bpm): "))
            timing = int(float(60000) / tempo)
                    
            #Valid Track Selected, Process Midi File
            print "Now Playing..."
            self.ProcessMidiTrack(tracks[trackno])

    def PlayKey(self, item):
        global canvas
        canvas.itemconfig(item, fill="#c0c0c0")
        canvas.addtag_withtag("graykey", item)
        
    def CreateKeys(self):
        global canvas
        global keyarray
        keyarray={}
        x = 30
        for i in range(21,108):
            if i % 12 != 1 and i % 12 != 3 and i % 12 != 6 and i % 12 != 8 and i % 12 != 10:
                keyarray[i] = canvas.create_rectangle(x, 10, x+20, 100, outline="#808080", fill="#ffffff", tags=("whitekey", str(i)))
                x=x+20
        x=45;
        for i in range (21,108):
            if i % 12 == 1 or i % 12 == 3 or i % 12 == 6 or i % 12 == 8 or i % 12 == 10:
                keyarray[i] = canvas.create_rectangle(x, 10, x+10, 60, outline="#808080", fill="#000000", tags=("blackkey", str(i)))
                x=x+20
            elif i % 12 == 4 or i % 12 == 11:
                x = x + 20
            

    def ClearKey(self, item):
        global canvas
        tags = canvas.gettags(item)
        for tag in tags:
            if tag=="whitekey":
                canvas.itemconfig(item, fill="#ffffff")
            if tag=="blackkey":
                canvas.itemconfig(item, fill="#000000")
        canvas.dtag(item, "graykey")

    #Process every note on/off event for the selected track and send it to MIDI output + GUI display
    def ProcessNoteEvent(self, event):
        global player
        pitch = event.data[0]
        velocity = event.data[1]

        if isinstance(event, midi.NoteOnEvent):
            player.note_on(pitch, velocity)
            self.PlayKey(keyarray[pitch])
        elif isinstance(event, midi.NoteOffEvent):
            player.note_off(pitch, velocity)
            self.ClearKey(keyarray[pitch])

    #Parse the list of notes in the selected track and process them with the correct timing
    def ProcessMidiTrack(self, selectedTrack):
        lastTick = 0
        index = 0
        tickno = 0
        wholeNote = timing * 4
            
        for event in selectedTrack:
            print str(event)
            if isinstance(event, midi.NoteEvent):
                notelist.append(event)

        while index < len(notelist):
            while index < len(notelist) and notelist[index].tick <= tickno - lastTick:
                self.ProcessNoteEvent(notelist[index])
                lastTick = tickno
                index += 1
            pygame.time.wait(wholeNote / 64)
            tickno += midiOutput.resolution * 4 / 64


def main():
    root = Tk()
    ex = Piano(root)
    root.geometry("1075x150+300+300")
    thread = threading.Thread(target=ex.initMidi)
    thread.start()
    root.mainloop()


if __name__ == '__main__':
    main()
