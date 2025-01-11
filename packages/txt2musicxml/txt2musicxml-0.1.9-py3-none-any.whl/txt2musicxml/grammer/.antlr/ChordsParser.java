// Generated from /Users/noamtamir/coding/txt2musicxml/txt2musicxml/grammer/Chords.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class ChordsParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		MEASURE_REPEAT=1, NOTE=2, ALTERATION=3, TIME_SIGNATURE=4, SUFFIX=5, SLASH=6, 
		REPEAT_BARLINE=7, DOUBLE_BARLINE=8, BARLINE=9, NEWLINE=10, WHITESPACE=11;
	public static final int
		RULE_sheet = 0, RULE_line = 1, RULE_bar = 2, RULE_chord_or_slash = 3, 
		RULE_chord = 4, RULE_slash = 5, RULE_root = 6, RULE_bass = 7, RULE_note = 8, 
		RULE_alteration = 9, RULE_suffix = 10, RULE_right_barlines = 11;
	private static String[] makeRuleNames() {
		return new String[] {
			"sheet", "line", "bar", "chord_or_slash", "chord", "slash", "root", "bass", 
			"note", "alteration", "suffix", "right_barlines"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'%'", null, null, null, null, "'/'", "':||'", "'||'", "'|'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "MEASURE_REPEAT", "NOTE", "ALTERATION", "TIME_SIGNATURE", "SUFFIX", 
			"SLASH", "REPEAT_BARLINE", "DOUBLE_BARLINE", "BARLINE", "NEWLINE", "WHITESPACE"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "Chords.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public ChordsParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SheetContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(ChordsParser.EOF, 0); }
		public List<LineContext> line() {
			return getRuleContexts(LineContext.class);
		}
		public LineContext line(int i) {
			return getRuleContext(LineContext.class,i);
		}
		public SheetContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sheet; }
	}

	public final SheetContext sheet() throws RecognitionException {
		SheetContext _localctx = new SheetContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_sheet);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(25); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(24);
				line();
				}
				}
				setState(27); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & 3158L) != 0) );
			setState(29);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LineContext extends ParserRuleContext {
		public TerminalNode NEWLINE() { return getToken(ChordsParser.NEWLINE, 0); }
		public List<BarContext> bar() {
			return getRuleContexts(BarContext.class);
		}
		public BarContext bar(int i) {
			return getRuleContext(BarContext.class,i);
		}
		public LineContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_line; }
	}

	public final LineContext line() throws RecognitionException {
		LineContext _localctx = new LineContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_line);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(32);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==NEWLINE) {
				{
				setState(31);
				match(NEWLINE);
				}
			}

			setState(35); 
			_errHandler.sync(this);
			_alt = 1;
			do {
				switch (_alt) {
				case 1:
					{
					{
					setState(34);
					bar();
					}
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(37); 
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,2,_ctx);
			} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BarContext extends ParserRuleContext {
		public Right_barlinesContext right_barlines() {
			return getRuleContext(Right_barlinesContext.class,0);
		}
		public List<Chord_or_slashContext> chord_or_slash() {
			return getRuleContexts(Chord_or_slashContext.class);
		}
		public Chord_or_slashContext chord_or_slash(int i) {
			return getRuleContext(Chord_or_slashContext.class,i);
		}
		public TerminalNode MEASURE_REPEAT() { return getToken(ChordsParser.MEASURE_REPEAT, 0); }
		public List<TerminalNode> WHITESPACE() { return getTokens(ChordsParser.WHITESPACE); }
		public TerminalNode WHITESPACE(int i) {
			return getToken(ChordsParser.WHITESPACE, i);
		}
		public TerminalNode TIME_SIGNATURE() { return getToken(ChordsParser.TIME_SIGNATURE, 0); }
		public BarContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bar; }
	}

	public final BarContext bar() throws RecognitionException {
		BarContext _localctx = new BarContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_bar);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(64);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,9,_ctx) ) {
			case 1:
				{
				{
				setState(40);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WHITESPACE) {
					{
					setState(39);
					match(WHITESPACE);
					}
				}

				setState(44);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==TIME_SIGNATURE) {
					{
					setState(42);
					match(TIME_SIGNATURE);
					setState(43);
					match(WHITESPACE);
					}
				}

				setState(46);
				chord_or_slash();
				setState(51);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
				while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
					if ( _alt==1 ) {
						{
						{
						setState(47);
						match(WHITESPACE);
						setState(48);
						chord_or_slash();
						}
						} 
					}
					setState(53);
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,5,_ctx);
				}
				setState(55);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WHITESPACE) {
					{
					setState(54);
					match(WHITESPACE);
					}
				}

				}
				}
				break;
			case 2:
				{
				{
				setState(58);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WHITESPACE) {
					{
					setState(57);
					match(WHITESPACE);
					}
				}

				setState(60);
				match(MEASURE_REPEAT);
				setState(62);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==WHITESPACE) {
					{
					setState(61);
					match(WHITESPACE);
					}
				}

				}
				}
				break;
			}
			setState(66);
			right_barlines();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Chord_or_slashContext extends ParserRuleContext {
		public ChordContext chord() {
			return getRuleContext(ChordContext.class,0);
		}
		public SlashContext slash() {
			return getRuleContext(SlashContext.class,0);
		}
		public Chord_or_slashContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chord_or_slash; }
	}

	public final Chord_or_slashContext chord_or_slash() throws RecognitionException {
		Chord_or_slashContext _localctx = new Chord_or_slashContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_chord_or_slash);
		try {
			setState(70);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case NOTE:
				enterOuterAlt(_localctx, 1);
				{
				setState(68);
				chord();
				}
				break;
			case SLASH:
				enterOuterAlt(_localctx, 2);
				{
				setState(69);
				slash();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ChordContext extends ParserRuleContext {
		public RootContext root() {
			return getRuleContext(RootContext.class,0);
		}
		public SuffixContext suffix() {
			return getRuleContext(SuffixContext.class,0);
		}
		public BassContext bass() {
			return getRuleContext(BassContext.class,0);
		}
		public ChordContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chord; }
	}

	public final ChordContext chord() throws RecognitionException {
		ChordContext _localctx = new ChordContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_chord);
		try {
			setState(83);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,11,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(72);
				root();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(73);
				root();
				setState(74);
				suffix();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(76);
				root();
				setState(77);
				bass();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(79);
				root();
				setState(80);
				suffix();
				setState(81);
				bass();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SlashContext extends ParserRuleContext {
		public TerminalNode SLASH() { return getToken(ChordsParser.SLASH, 0); }
		public SlashContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_slash; }
	}

	public final SlashContext slash() throws RecognitionException {
		SlashContext _localctx = new SlashContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_slash);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(85);
			match(SLASH);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RootContext extends ParserRuleContext {
		public NoteContext note() {
			return getRuleContext(NoteContext.class,0);
		}
		public AlterationContext alteration() {
			return getRuleContext(AlterationContext.class,0);
		}
		public RootContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_root; }
	}

	public final RootContext root() throws RecognitionException {
		RootContext _localctx = new RootContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_root);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(87);
			note();
			setState(89);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ALTERATION) {
				{
				setState(88);
				alteration();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BassContext extends ParserRuleContext {
		public TerminalNode SLASH() { return getToken(ChordsParser.SLASH, 0); }
		public NoteContext note() {
			return getRuleContext(NoteContext.class,0);
		}
		public AlterationContext alteration() {
			return getRuleContext(AlterationContext.class,0);
		}
		public BassContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bass; }
	}

	public final BassContext bass() throws RecognitionException {
		BassContext _localctx = new BassContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_bass);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(91);
			match(SLASH);
			setState(92);
			note();
			setState(94);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ALTERATION) {
				{
				setState(93);
				alteration();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class NoteContext extends ParserRuleContext {
		public TerminalNode NOTE() { return getToken(ChordsParser.NOTE, 0); }
		public NoteContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_note; }
	}

	public final NoteContext note() throws RecognitionException {
		NoteContext _localctx = new NoteContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_note);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(96);
			match(NOTE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AlterationContext extends ParserRuleContext {
		public TerminalNode ALTERATION() { return getToken(ChordsParser.ALTERATION, 0); }
		public AlterationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_alteration; }
	}

	public final AlterationContext alteration() throws RecognitionException {
		AlterationContext _localctx = new AlterationContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_alteration);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(98);
			match(ALTERATION);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SuffixContext extends ParserRuleContext {
		public TerminalNode SUFFIX() { return getToken(ChordsParser.SUFFIX, 0); }
		public SuffixContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_suffix; }
	}

	public final SuffixContext suffix() throws RecognitionException {
		SuffixContext _localctx = new SuffixContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_suffix);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(100);
			match(SUFFIX);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Right_barlinesContext extends ParserRuleContext {
		public TerminalNode BARLINE() { return getToken(ChordsParser.BARLINE, 0); }
		public TerminalNode DOUBLE_BARLINE() { return getToken(ChordsParser.DOUBLE_BARLINE, 0); }
		public TerminalNode REPEAT_BARLINE() { return getToken(ChordsParser.REPEAT_BARLINE, 0); }
		public Right_barlinesContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_right_barlines; }
	}

	public final Right_barlinesContext right_barlines() throws RecognitionException {
		Right_barlinesContext _localctx = new Right_barlinesContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_right_barlines);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(102);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 896L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001\u000bi\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0001"+
		"\u0000\u0004\u0000\u001a\b\u0000\u000b\u0000\f\u0000\u001b\u0001\u0000"+
		"\u0001\u0000\u0001\u0001\u0003\u0001!\b\u0001\u0001\u0001\u0004\u0001"+
		"$\b\u0001\u000b\u0001\f\u0001%\u0001\u0002\u0003\u0002)\b\u0002\u0001"+
		"\u0002\u0001\u0002\u0003\u0002-\b\u0002\u0001\u0002\u0001\u0002\u0001"+
		"\u0002\u0005\u00022\b\u0002\n\u0002\f\u00025\t\u0002\u0001\u0002\u0003"+
		"\u00028\b\u0002\u0001\u0002\u0003\u0002;\b\u0002\u0001\u0002\u0001\u0002"+
		"\u0003\u0002?\b\u0002\u0003\u0002A\b\u0002\u0001\u0002\u0001\u0002\u0001"+
		"\u0003\u0001\u0003\u0003\u0003G\b\u0003\u0001\u0004\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0003\u0004T\b\u0004\u0001\u0005\u0001"+
		"\u0005\u0001\u0006\u0001\u0006\u0003\u0006Z\b\u0006\u0001\u0007\u0001"+
		"\u0007\u0001\u0007\u0003\u0007_\b\u0007\u0001\b\u0001\b\u0001\t\u0001"+
		"\t\u0001\n\u0001\n\u0001\u000b\u0001\u000b\u0001\u000b\u0000\u0000\f\u0000"+
		"\u0002\u0004\u0006\b\n\f\u000e\u0010\u0012\u0014\u0016\u0000\u0001\u0001"+
		"\u0000\u0007\tl\u0000\u0019\u0001\u0000\u0000\u0000\u0002 \u0001\u0000"+
		"\u0000\u0000\u0004@\u0001\u0000\u0000\u0000\u0006F\u0001\u0000\u0000\u0000"+
		"\bS\u0001\u0000\u0000\u0000\nU\u0001\u0000\u0000\u0000\fW\u0001\u0000"+
		"\u0000\u0000\u000e[\u0001\u0000\u0000\u0000\u0010`\u0001\u0000\u0000\u0000"+
		"\u0012b\u0001\u0000\u0000\u0000\u0014d\u0001\u0000\u0000\u0000\u0016f"+
		"\u0001\u0000\u0000\u0000\u0018\u001a\u0003\u0002\u0001\u0000\u0019\u0018"+
		"\u0001\u0000\u0000\u0000\u001a\u001b\u0001\u0000\u0000\u0000\u001b\u0019"+
		"\u0001\u0000\u0000\u0000\u001b\u001c\u0001\u0000\u0000\u0000\u001c\u001d"+
		"\u0001\u0000\u0000\u0000\u001d\u001e\u0005\u0000\u0000\u0001\u001e\u0001"+
		"\u0001\u0000\u0000\u0000\u001f!\u0005\n\u0000\u0000 \u001f\u0001\u0000"+
		"\u0000\u0000 !\u0001\u0000\u0000\u0000!#\u0001\u0000\u0000\u0000\"$\u0003"+
		"\u0004\u0002\u0000#\"\u0001\u0000\u0000\u0000$%\u0001\u0000\u0000\u0000"+
		"%#\u0001\u0000\u0000\u0000%&\u0001\u0000\u0000\u0000&\u0003\u0001\u0000"+
		"\u0000\u0000\')\u0005\u000b\u0000\u0000(\'\u0001\u0000\u0000\u0000()\u0001"+
		"\u0000\u0000\u0000),\u0001\u0000\u0000\u0000*+\u0005\u0004\u0000\u0000"+
		"+-\u0005\u000b\u0000\u0000,*\u0001\u0000\u0000\u0000,-\u0001\u0000\u0000"+
		"\u0000-.\u0001\u0000\u0000\u0000.3\u0003\u0006\u0003\u0000/0\u0005\u000b"+
		"\u0000\u000002\u0003\u0006\u0003\u00001/\u0001\u0000\u0000\u000025\u0001"+
		"\u0000\u0000\u000031\u0001\u0000\u0000\u000034\u0001\u0000\u0000\u0000"+
		"47\u0001\u0000\u0000\u000053\u0001\u0000\u0000\u000068\u0005\u000b\u0000"+
		"\u000076\u0001\u0000\u0000\u000078\u0001\u0000\u0000\u00008A\u0001\u0000"+
		"\u0000\u00009;\u0005\u000b\u0000\u0000:9\u0001\u0000\u0000\u0000:;\u0001"+
		"\u0000\u0000\u0000;<\u0001\u0000\u0000\u0000<>\u0005\u0001\u0000\u0000"+
		"=?\u0005\u000b\u0000\u0000>=\u0001\u0000\u0000\u0000>?\u0001\u0000\u0000"+
		"\u0000?A\u0001\u0000\u0000\u0000@(\u0001\u0000\u0000\u0000@:\u0001\u0000"+
		"\u0000\u0000AB\u0001\u0000\u0000\u0000BC\u0003\u0016\u000b\u0000C\u0005"+
		"\u0001\u0000\u0000\u0000DG\u0003\b\u0004\u0000EG\u0003\n\u0005\u0000F"+
		"D\u0001\u0000\u0000\u0000FE\u0001\u0000\u0000\u0000G\u0007\u0001\u0000"+
		"\u0000\u0000HT\u0003\f\u0006\u0000IJ\u0003\f\u0006\u0000JK\u0003\u0014"+
		"\n\u0000KT\u0001\u0000\u0000\u0000LM\u0003\f\u0006\u0000MN\u0003\u000e"+
		"\u0007\u0000NT\u0001\u0000\u0000\u0000OP\u0003\f\u0006\u0000PQ\u0003\u0014"+
		"\n\u0000QR\u0003\u000e\u0007\u0000RT\u0001\u0000\u0000\u0000SH\u0001\u0000"+
		"\u0000\u0000SI\u0001\u0000\u0000\u0000SL\u0001\u0000\u0000\u0000SO\u0001"+
		"\u0000\u0000\u0000T\t\u0001\u0000\u0000\u0000UV\u0005\u0006\u0000\u0000"+
		"V\u000b\u0001\u0000\u0000\u0000WY\u0003\u0010\b\u0000XZ\u0003\u0012\t"+
		"\u0000YX\u0001\u0000\u0000\u0000YZ\u0001\u0000\u0000\u0000Z\r\u0001\u0000"+
		"\u0000\u0000[\\\u0005\u0006\u0000\u0000\\^\u0003\u0010\b\u0000]_\u0003"+
		"\u0012\t\u0000^]\u0001\u0000\u0000\u0000^_\u0001\u0000\u0000\u0000_\u000f"+
		"\u0001\u0000\u0000\u0000`a\u0005\u0002\u0000\u0000a\u0011\u0001\u0000"+
		"\u0000\u0000bc\u0005\u0003\u0000\u0000c\u0013\u0001\u0000\u0000\u0000"+
		"de\u0005\u0005\u0000\u0000e\u0015\u0001\u0000\u0000\u0000fg\u0007\u0000"+
		"\u0000\u0000g\u0017\u0001\u0000\u0000\u0000\u000e\u001b %(,37:>@FSY^";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}