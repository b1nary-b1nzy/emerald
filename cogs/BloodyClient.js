const Discord = require('discord.js');
const Command = require("./structures/Command.js");
const CommandStore = require("./structures/CommandStore.js");
const AliasStore = require("./structures/AliasStore.js");
const Inhibitor = require("./structures/Inhibitor.js"); // eslint-disable-line
const InhibitorStore = require("./structures/InhibitorStore.js"); // eslint-disable-line
const klaw = require("klaw");
const chalk = require("chalk").default;
const { join, parse, sep } = require("path");
const fs = require("fs");
const { ncp } = require("ncp"); // eslint-disable-line

class BloodyCord extends Discord.Client {
    constructor(clientOptions) {
        super()
        this.clientOptions = clientOptions;

        /**
         * Stores the bots commands.
         * @type {Map<String, Command>}
         */
        this.commands = new CommandStore();

        /**
         * Stores the bots aliases
         * @type {Map<String, Command>}
         */
        this.aliases = new AliasStore();

        /**
         * Stores the inhubitors when a command is run.
         * @type {Map<String, Command>}
         */
        this.inhibitors = new InhibitorStore();
    }

    /**
     * Loads the options for the bot. Such as: Owner ID, readyMessage, and more.
     * @param {Object} clientOptions
     */
    async _loadOptions({ prefix, withTyping, ownerId, readyMessage, game } = {}) {
        const app = await this.fetchApplication();

        /**
         * Default prefix:
         * @default "-"
         */
        this.prefix = prefix || "-";

        /**
         * A bool to determine if bot should/not type during commands
         * @default true;
         */
        this.withTyping = withTyping || true;

        /**
         * Default owner ID 
         * Gets default if none named
         * Gets from bot application
         */
        this.ownerId = ownerId || app.ownerId;

        /**
         * Default 'on' message
         * @default "${tag} is serving ${guilds} servers, ${channels} channels, and ${users} users!"
         */
        this.readyMessage = readyMessage(this) || "${tag} is serving ${guilds} servers, ${channels} channels, and ${users} users!";

        /**
         * Default status
         * @default "Streaming with ${guilds} guilds | ${prefix}help"
         */
        this.game = game || { url: "https://twitch.tv/scarecrowboat", name: `with ${this.guilds.size > 1 ? `${this.guilds.size} guilds`}

        /**
         * Gotta log the bot in *thonks*
         * Also gotta load those sexy commands *orgys*
         * OOF! Has ready, and message listeners 
         * @param {string} token Token, DUH!
         * @returns {Promise<string>} Logged in
         */
        async login(token) {
            this._extractCommands();
            this._extractInhibitors();
            //Dem Listeners doe
            this._attachEvents();
            return super.login(token);
        }

        /**
         * Gets category, that way all commands arent in one big category
         * Cleans up that dope asf help command
         * @param {string} parsedPath the path, duh
         * @returns {string} category
         */
        _getCategory(parsedPath) {
            const dirs = fs.readdirSync("./commands/");
            for (let i = 0; i < dirs.length; i++) {
                for (const pathSplit of parsedPath.split("\\")) {
                    if (pathSplit === dirs[i]) return dirs[i];
                }
            }
        }

        /**@private */
        _attachEvents() {
            this.on('ready', async () => {
                await this._loadOptions(this._loadOptions);
                if (typeof this.game.name === "function") {
                    this.user.setActivity(this.game.name(this), { url: this.game.url, type: this.game.type });
                } else {
                    this.user.setActivity(this.game.name, { url: this.game.url, type: this.game.type });
                }
                console.log(`${chalk.bgBlueBright("INFO")} ${this.readyMessage}`);
            });
            this.on("message", message => this._handleMessage(message));
            process.on("unhandledRejection", e => console.log(`${chalk.bgRedBright("ERROR")}${chalk.redBright(e.stack)}`));
        }

        /**@private */
        _extractCommands() {
            if (!fs.existsSync(join(__dirname, "..", "..", "..", "commands"))) {
                fs.mkdir(join(__dirname, "..", "..", "..", "commands", "."), () => {
                    ncp(join(__dirname, ".", "commands"), join(__dirname, "..", "..", "..", "commands", "."), () => {
                        this._loadCommands();
                    });
                });
            } else { this._loadCommands(); }
        }

        /**@private */
        _extractInhibitors() {
            if (!fs.existsSync(join(__dirname, "..", "..", "..", "inhibitors"))) {
                fs.mkdir(join(__dirname, "..", "..", "..", "inhibitors", "."), () => {
                    ncp(join(__dirname, ".", "inhibitors"), join(__dirname, "..", "..", "..", "inhibitors", "."), () => {
                        this._loadInhibitors();
                    });
                });
            } else { this._loadInhibitors(); }
        }

        /**
         * Loads a command.
         * @param {string} path The path to command.
         * @param {string} commadn file to load.
         * @private
         */
        _loadCommand(path, command) {
            const c = new (require(`${path}${sep}${command}`))(this);
            this.commands.set(c.name, c);
            this.commands.get(c.name).category = this. _getCategory(path);
            for (const alias of c.aliases) {
                this.aliases.set(alias, c);
            }
        }
        /**
         * Load commands w/ aliases
         * @private
         */
        _loadCommands() {
            const started = Date.now();
            klaw("./commands")
                .on("data", commandFile => {
                    const cmd = parse(commandFile.path);
                    if(!cmd.exit || cmd.exit !== ".js") return;
                    return this._loadCommand(cmd.dir, cmd.name);
                })
                .on("end", () => {
                    console.log(`${chalk.bgBlueBright("INFO")} Loaded ${this.commands.size} commands, and ${this.aliases.size} aliases in ${(Date.now() - started).toFixed(2)}ms.`);
            });
        }

    }
}
